import logging
import os
import argparse

import pluggy

from flask import jsonify, make_response, request
    
from jumonc.handlers.base import api_version_path, check_version, RESTAPI, return_schema, get_return_schema_description
from jumonc.authentication import scopes
from jumonc.authentication.check import check_auth
    
import jumonc.handlers.versionTree as tree
from jumonc import settings


from jumonc_llview import verifyLLView


__name__ = "llview"

logger = logging.getLogger(__name__)

hookimpl = pluggy.HookimplMarker("jumonc")


links = []

paths = []



@hookimpl
def needed_REST_paths():
    return [api_version_path + "/llview",]


@hookimpl
def register_REST_path(requested_path, approved_path):
    
    tree.links["v1"].append({
                "link": "/v1/llview",
                "isOptional": True,
                "description": "Following this links leads to the llview jumonc plugin ",
                "parameters": [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
            })
    
    
    links.append({
                "link": "/v1/llview/paths",
                "isOptional": True,
                "description": "Following this links leads to the API paths to be used by LLVIEW",
                "parameters": [
                    {"name": "token",
                    "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
                ]
            })
    
    
    links.append({
                "link": "/v1/llview/retrieveToken",
                "isOptional": True,
                "description": "Following this links leads to the API paths to be used by LLVIEW",
                "parameters": [
                    {"name": "getMessage",
                    "description": "Get a message to verify using the private key"},
                    {"name": "VerifiedMessage",
                    "description": "Send the verified message, if valid get access token"}
                ]
            })
    
    
    @RESTAPI.route(approved_path, methods=["GET"])
    @check_version
    @check_auth(scopes["see_links"])
    def llview_links(version):
        logger.debug("Accessed /v%i/llview/", version)
        return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)
    
    
    @RESTAPI.route(approved_path + "/paths", methods=["GET"])
    @check_version
    @check_auth(scopes["compute_data"])
    def llview_paths(version):
        return make_response(jsonify({"paths": paths}), 200)

    
    @RESTAPI.route(approved_path + "/retrieveToken", methods=["GET"])
    @check_version
    def llview_retrieveToken(version):
        getMessage = request.args.get('getMessage', default = False, type = settings.helpers.parse_boolean)
        verifiedMessage = request.args.get('VerifiedMessage', default = "", type = str)
        if getMessage:
            return verifyLLView.getMessage()
        if verifiedMessage:
            return verifyLLView.testMessage(verifiedMessage)
        return make_response(jsonify({"Neither getMessage or VerifiedMessage message argument found": paths}), 400)


@hookimpl
def startup_parameter_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=("jumonc llview plugin"), prog="jumonc --llview")

    parser.add_argument("--API-PATHS".lower(), 
                       dest="API_PATHS", 
                       help="Set API paths that can be querried by llview for the job reporting", 
                       default=[],
                       nargs='*',
                       type=str)
    parser.add_argument("--KEY-PATH".lower(), 
                       dest="KEY_PATH", 
                       help="Set path to  public key to verify LLView as communication partner", 
                       default=None,
                       type=str)
    parser.add_argument("--LLVIEW-SCOPE-LEVEL".lower(), 
                       dest="LLVIEW_SCOPE_LEVEL", 
                       help="Set scope level that for the token retrieved by LLView", 
                       default=5,
                       type=int)
    return parser
    

@hookimpl
def evaluate_startup_parameter(parsed:argparse.Namespace) -> None:
    global paths
    
    paths = paths + parsed.API_PATHS
    
    if parsed.KEY_PATH is not None:
        verifyLLView.readKey(parsed.KEY_PATH, parsed.LLVIEW_SCOPE_LEVEL)

    
    

@hookimpl
def register_MPI(MPI_ID_min, MPI_ID_max):
    pass


@hookimpl
def selfcheck_is_working():
    return True
