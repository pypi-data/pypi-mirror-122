import datetime
import json
from dataclasses import dataclass
from functools import partial
from itertools import starmap
from pprint import pformat
from typing import Any, Dict, Iterator, List, TypeVar, Union

import rdflib
from boltons.iterutils import remap
from documented import DocumentedError
from pyld.jsonld import JsonLdError

from iolanta.models import LDContext, LDDocument
from octadocs.octiron.context import merge
from octadocs.pyld_document_loaders.choice import ChoiceLoader
from octadocs.pyld_document_loaders.named import NamedLoader
from octadocs.types import LOCAL, Context, Triple
from pyld import jsonld
from pyld.documentloader.requests import requests_document_loader

try:  # noqa
    from yaml import CSafeDumper as SafeDumper  # noqa
    from yaml import CSafeLoader as SafeLoader  # noqa
except ImportError:
    from yaml import SafeDumper  # type: ignore   # noqa
    from yaml import SafeLoader  # type: ignore   # noqa


MetaData = Union[List[Dict[str, Any]], Dict[str, Any]]   # type: ignore  # noqa

Data = TypeVar('Data')


@dataclass
class ExpandError(DocumentedError):
    """
    JSON-LD expand operation failed.

    {self.message}

    Data: {self.formatted_data}
    Context: {self.formatted_context}
    IRI: {self.iri}
    """

    message: str
    document: LDDocument
    context: LDContext
    iri: str

    @property
    def formatted_data(self) -> str:
        """Format document for printing."""
        return json.dumps(self.document, indent=2)

    @property
    def formatted_context(self):
        """Format context for printing."""
        return json.dumps(self.context, indent=2)


def _convert(term: Any) -> Any:  # type: ignore
    """Convert $statement to @statement."""
    if isinstance(term, str) and term.startswith('$'):
        return '@' + term[1:]  # noqa: WPS336

    # pyld cannot expand() a document which contains data which cannot be
    # trivially serialized to JSON.
    # FIXME we may want to replace this with an xsd:date declaration, but let's
    #   revisit that later.
    if isinstance(term, (datetime.date, datetime.datetime)):
        return str(term)

    return term


def convert_dollar_signs(
    meta_data: Data,
) -> Data:
    """
    Convert $ character to @ in keys.

    We use $ by convention to avoid writing quotes.
    """
    if not meta_data:
        return {}

    return remap(
        meta_data,
        lambda path, key, value: (  # noqa: WPS110
            _convert(key),
            _convert(value),
        ),
    )


def as_triple_stream(
    raw_data: MetaData,
    context: Context,
    local_iri: str,
    named_contexts: Dict[str, Any],
    blank_node_prefix: str = '',
) -> Iterator[Triple]:
    """Convert YAML dict to a stream of triples."""
    if isinstance(raw_data, list):
        yield from _list_as_triple_stream(
            context=context,
            local_iri=local_iri,
            raw_data=raw_data,
            named_contexts=named_contexts,
            blank_node_prefix=blank_node_prefix,
        )

    elif isinstance(raw_data, dict):
        yield from _dict_as_triple_stream(
            context=context,
            local_iri=local_iri,
            raw_data=raw_data,
            named_contexts=named_contexts,
            blank_node_prefix=blank_node_prefix,
        )

    else:
        raise ValueError(f'Format of data not recognized: {raw_data}')


def reformat_blank_nodes(prefix: str, triple: Triple) -> Triple:
    """
    Prepend prefix to every blank node.

    JSON-LD flattening creates sequential identifiers in the form of _:bN
    for every blank node. See https://www.w3.org/TR/json-ld11/

    This means that subgraphs of the Octiron ConjunctiveGraph have clashing
    blank node identifiers.

    To avoid that, we prepend a prefix to every blank node identifier.
    """
    return Triple(*(
        rdflib.BNode(value=prefix + str(singleton)) if (
            isinstance(singleton, rdflib.BNode)
        ) else singleton
        for singleton in triple
    ))


def _dict_as_triple_stream(  # type: ignore
    raw_data: LDDocument,
    context: LDContext,
    local_iri: str,
    named_contexts: Dict[str, LDContext],
    blank_node_prefix: str = '',
) -> Iterator[Triple]:
    """Convert dict into a triple stream."""
    meta_data = convert_dollar_signs(raw_data)

    local_context = meta_data.pop('@context', None)
    if isinstance(local_context, str):
        try:
            local_context = named_contexts[local_context]
        except KeyError as err:
            raise ValueError(
                f'Named context {local_context} is unknown.',
            ) from err

    if local_context is not None:
        context = merge(
            first=context,
            second=local_context,
        )

    if meta_data.get('@id') is None:
        # The document author did not tell us about what their document is.
        # In this case, we assume that the local_iri of the document file
        # is the subject of the document description.
        meta_data['@id'] = local_iri

    # The author specified an IRI the document tells us about. Let us
    # link this IRI to the local document IRI.
    meta_data['subjectOf'] = local_iri

    # Reason: https://github.com/RDFLib/rdflib-jsonld/issues/97
    # If we don't expand with an explicit @base, import will fail silently.
    try:
        meta_data = jsonld.expand(
            meta_data,
            options={
                'base': str(LOCAL),
                'expandContext': context,
                'documentLoader': ChoiceLoader(loaders=[
                     NamedLoader(documents=named_contexts),
                     requests_document_loader(),
                ]),
            },
        )
    except (TypeError, JsonLdError) as err:
        raise ExpandError(
            message=str(err),
            document=meta_data,
            context=context,
            iri=local_iri,
        ) from err

    # Reason: https://github.com/RDFLib/rdflib-jsonld/issues/98
    # If we don't flatten, @included sections will not be imported.
    meta_data = jsonld.flatten(meta_data)
    serialized_meta_data = json.dumps(meta_data, indent=4)

    graph = rdflib.Graph()
    graph.parse(
        data=serialized_meta_data,
        format='json-ld',
    )
    yield from map(
        partial(
            reformat_blank_nodes,
            f'{local_iri}/{blank_node_prefix}',
        ),
        starmap(
            Triple,
            iter(graph),
        ),
    )


def _list_as_triple_stream(  # type: ignore
    raw_data: List[Dict[str, Any]],
    context: Context,
    local_iri: str,
    named_contexts: Dict[str, Any],
    blank_node_prefix: str = '',
) -> Iterator[Triple]:
    """Convert a list into a triple stream."""
    for sub_document_number, sub_document in enumerate(raw_data):
        yield from as_triple_stream(
            raw_data=sub_document,
            context=context,
            local_iri=local_iri,
            named_contexts=named_contexts,
            blank_node_prefix=f'{blank_node_prefix}_{sub_document_number}',
        )
