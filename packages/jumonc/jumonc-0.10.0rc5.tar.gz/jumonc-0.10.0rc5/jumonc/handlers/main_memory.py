import logging
from typing import Dict
from typing import List
from typing import Union

from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from flask import Response

import jumonc.models.cache.helper as cache
from jumonc import settings
from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
from jumonc.handlers.base import api_version_path
from jumonc.handlers.base import check_version
from jumonc.handlers.base import generate_cache_id
from jumonc.handlers.base import get_prefer_id_description
from jumonc.handlers.base import RESTAPI
from jumonc.models import pluginInformation
from jumonc.tasks import memory


logger = logging.getLogger(__name__)

links:        List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
status_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
config_links: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

main_memory_path = "/main_memory"

@RESTAPI.route(api_version_path + main_memory_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnMainMemoryLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/main_memory/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + main_memory_path + "/status", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnMemoryStatusLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/main_memory/status", version)
    return make_response(jsonify(sorted(status_links, key=lambda dic: dic['link'])), 200)

@RESTAPI.route(api_version_path + main_memory_path + "/config", methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnMemoryConfigLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/main_memory/config", version)
    return make_response(jsonify(sorted(config_links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    links.append(registerStatusLinks(version))
    links.append(registerConfigLinks(version))
    return {
        "link": "/v" + str(version) + main_memory_path,
        "isOptional": False,
        "description": "Gather information about the main memory",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerStatusLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    types : List[str] = ["free", "used"]
    descriptions : List[str] = ["Get the average free memory on your nodes", "Get the average free memeory on your nodes"]
    if pluginInformation.pluginIsWorking("jumonc_memoryPlugin") is True:
        parameters = [  {"name": "duration",
                        "description": "When this parameter is not present the raw data value(s) will be provided, otherwise the average value per second"},
                        {"name": "humanReadable",
                        "description": "For 'True' convert to better readable numbers, for 'False' return actual number. " + 
                        "If not set to valid value, uses default value(" + str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) + ")."},
                        {"name": "node",
                        "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                        {"name": "token",
                        "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
                
        parameters.append(get_prefer_id_description())
        
        for i, typeStr in enumerate(types):
            status_links.append({
            "link": "/v" + str(version) + main_memory_path + "/status/" + typeStr,
            "isOptional": True,
            "description": descriptions[i],
            "parameters": parameters
            })
        
        @RESTAPI.route(api_version_path + main_memory_path + "/status/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        @generate_cache_id
        def returnMemoryStatus(version: int, datatype:str, cache_id:int) -> Response:
            duration = request.args.get('duration', default = -1.0, type = float)
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/main_memory/status/%s", version, datatype)
            
            if duration >0:
                cache.addParameter(cache_id, "duration", str(duration))
                cache.commit()
            
            data = memory.plugin.getStatusData(dataType = datatype,
                                               duration = duration,
                                               overrideHumanReadableWithValue = humanReadable)
            if len(data) > 0:
                for data_element in data:
                    for result_name, result in data_element.items():
                        cache.addResult(cache_id, result_name, result)
                cache.commit()
                return make_response(jsonify(data), 200)
            
            logger.warning("Accessed /v%i/main_memory/status/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + main_memory_path + "/status",
        "isOptional": False,
        "description": "Gather information concerning the memory status",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }


def registerConfigLinks(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    types : List[str] = ["total"]
    descriptions : List[str] = ["Get the average total memory on your nodes"]
    if pluginInformation.pluginIsWorking("jumonc_memoryPlugin") is True:
        for i, typeStr in enumerate(types):
            config_links.append({
            "link": "/v" + str(version) + main_memory_path + "/config/" + typeStr,
            "isOptional": True,
            "description": descriptions[i],
            "parameters": [
                {"name": "duration",
                "description": "When this parameter is not present the raw data value(s) will be provided, otherwise the average value per second"},
                {"name": "humanReadable",
                "description": "For 'True' convert to better readable numbers, for 'False' return actual number. " + 
                 "If not set to valid value, uses default value(" + str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) + ")."},
                {"name": "node",
                "description": "When this parameter is not present the average data of all nodes is presented, otherwise only from the choosen node"},
                {"name": "token",
                "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
            })
        
        @RESTAPI.route(api_version_path + main_memory_path + "/config/<string:datatype>", methods=["GET"])
        @check_version
        @check_auth(scopes["compute_data"])
        def returnMemoryConfig(version: int, datatype:str) -> Response:
            humanReadable = request.args.get('humanReadable', default = settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS, type = settings.helpers.parse_boolean)
            logger.debug("Accessed /v%i/main_memory/config/%s", version, datatype)
            data = memory.plugin.getConfigData(dataType = datatype, overrideHumanReadableWithValue = humanReadable)
            if len(data) > 0:
                return make_response(jsonify(data), 200)
            
            logger.warning("Accessed /v%i/main_memory/config/%s, but not avaiable", version, datatype)
            abort(404)
            return make_response("",404)
        
    return {
        "link": "/v" + str(version) + main_memory_path + "/config",
        "isOptional": False,
        "description": "Gather information concerning the memory config",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
