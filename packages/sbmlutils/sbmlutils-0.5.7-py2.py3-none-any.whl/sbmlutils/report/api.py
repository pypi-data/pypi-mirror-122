"""API for the sbmlreport web service.

This provides basic functionality of
parsing the model and returning the JSON representation based on fastAPI.
"""
import json
import time
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pymetadata.core.annotation import RDFAnnotation, RDFAnnotationData
from pymetadata.identifiers.miriam import BQB

from sbmlutils import log
from sbmlutils.console import console
from sbmlutils.report.api_examples import ExampleMetaData, examples_info
from sbmlutils.report.sbmlinfo import SBMLDocumentInfo


logger = log.get_logger(__name__)

api = FastAPI(
    #     root_path="/api/v1",
    #    openapi_prefix="/api/v1",
    title="sbml4humans",
    description="sbml4humans backend api",
    version="0.1.1",
    terms_of_service="https://github.com/matthiaskoenig/sbmlutils/blob/develop/sbml4humans/privacy_notice.md",
    contact={
        "name": "Matthias König",
        "url": "https://livermetabolism.com",
        "email": "konigmatt@googlemail.com",
    },
    license_info={
        "name": "LGPLv3",
        "url": "http://opensource.org/licenses/LGPL-3.0",
    },
    openapi_tags=[
        {
            "name": "examples",
            "description": "Manage and query examples.",
        },
        {
            "name": "metadata",
            "description": "Manage and query metadata.",
        },
        {
            "name": "reports",
            "description": "Create report data.",
        },
    ],
)


# API Permissions Data
origins = [
    # "localhost",
    # "localhost:3456",
    # "sbml4humans.de",
    "*"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/api/examples", tags=["examples"])
def examples() -> Dict[Any, Any]:
    """Get examples for reports."""
    try:
        example: ExampleMetaData
        return {"examples": [example.dict() for example in examples_info.values()]}

    except Exception as e:
        return _handle_error(e)


@api.get("/api/examples/{example_id}", tags=["examples"])
def example(example_id: str) -> Dict[Any, Any]:
    """Get specific example."""
    uid = uuid.uuid4().hex
    try:
        example: Optional[ExampleMetaData] = examples_info.get(example_id, None)
        content: Dict
        if example:
            source: Path = example.file  # type: ignore
            content = json_for_sbml(uid, source=source)
        else:
            content = {"error": f"example for id does not exist '{example_id}'"}

        return content
    except Exception as e:
        return _handle_error(e)


@api.post("/api/file", tags=["reports"])
async def report_from_file(request: Request) -> Dict[Any, Any]:
    """Upload file and return JSON report."""
    uid = uuid.uuid4().hex
    try:
        file_data = await request.form()
        file_content = await file_data["source"].read()  # type: ignore
        return json_for_sbml(uid, source=file_content)

    except Exception as e:
        return _handle_error(e, info={"uid": uid})


@api.get("/api/url", tags=["reports"])
def report_from_url(url: str) -> Dict[Any, Any]:
    """Get JSON report via URL."""
    uid = uuid.uuid4().hex
    try:
        response = requests.get(url)
        response.raise_for_status()
        return json_for_sbml(uid, source=response.text)

    except Exception as e:
        return _handle_error(e, info={"uid": str(uid), "url": url})


@api.post("/api/content", tags=["reports"])
async def get_report_from_content(request: Request) -> Dict[Any, Any]:
    """Get JSON report from file contents."""
    uid: str = uuid.uuid4().hex
    file_content: Optional[str] = None
    try:
        file_content_bytes: bytes = await request.body()
        file_content = file_content_bytes.decode("utf-8")
        return json_for_sbml(uid, source=file_content)

    except Exception as e:
        return _handle_error(e, info={"uid": uid, "content": str(file_content)})


def json_for_sbml(uid: str, source: Union[Path, str, bytes]) -> Dict:
    """Create JSON content for given SBML source.

    Source is either path to SBML file or SBML string.
    """

    if isinstance(source, bytes):
        source = source.decode("utf-8")

    time_start = time.time()
    info = SBMLDocumentInfo.from_sbml(source=source)
    time_elapsed = round(time.time() - time_start, 3)

    debug = False
    if debug:
        console.rule("Creating JSON content")
        console.print(info.info)
        console.rule()

    logger.info(f"JSON created for '{uid}' in '{time_elapsed}'")

    return {
        "report": info.info,
        "debug": {
            "jsonReportTime": f"{time_elapsed} [s]",
        },
    }


def _handle_error(e: Exception, info: Optional[Dict] = None) -> Dict[Any, Any]:
    """Handle exceptions in the backend.

    All calls are wrapped in a try/except which will provide the errors to the frontend.

    :param info: optional dictionary with information.
    """
    res = {
        "errors": [
            f"{e.__str__()}",
            f"{''.join(traceback.format_exception(None, e, e.__traceback__))}",
        ],
        "warnings": [],
        "info": info,
    }

    return res


@api.get("/api/annotation_resource", tags=["metadata"])
def get_annotation_resource(resource: str) -> Dict[Any, Any]:
    """Get information for annotation_resource.

    Used to resolve annotation information.

    :param resource: unique identifier of resource (url or miriam urn)
    :return: Response
    """
    try:
        annotation = RDFAnnotation(qualifier=BQB.IS, resource=resource)
        data = RDFAnnotationData(annotation=annotation)
        return data.to_dict()  # type: ignore

    except Exception as e:
        return _handle_error(e)


if __name__ == "__main__":
    # shell command: uvicorn sbmlutils.report.api:app --reload --port 1444
    uvicorn.run(
        "sbmlutils.report.api:api",
        host="localhost",
        port=1444,
        log_level="info",
        reload=True,
    )
