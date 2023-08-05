import inspect
import json
import pathlib
import os
import warnings
import pydantic
import importlib
import sys
from typing import Union, Dict, List

from .exceptions import NodeNotFoundException


class BaseNode(object):

    def __eq__(self, other):
        if hasattr(other, 'unique_id'):
            return self.unique_id == other.unique_id
        elif type(other) == str:
            return self.unique_id == other
        else:
            return False

    def __hash__(self):
        return hash(self.unique_id)

    def __repr__(self):
        return f"<Node {self.unique_id}>"

    @property
    def project(self):
        return Project

    @property
    def manifest_node(self):
        return self.project.manifest.nodes[self]

    @property
    def catalog_node(self):
        return self.manifest.nodes[self]


class NodeReference(BaseNode):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError(f'Node reference must be a string, got {type(v)}')
        else:
            return cls(unique_id=v)

    def __init__(self, unique_id):
        self.unique_id = unique_id

    def __getattr__(self, attr):
        if attr in dir(self.manifest_node):
            return getattr(self.manifest_node, attr)
        else:
            raise AttributeError

    def __repr__(self):
        return f"<Node {self.unique_id}>"

    def __str__(self):
        return f"<Node {self.unique_id}>"


class DependsOn(pydantic.BaseModel):
    nodes: List[NodeReference]
    macros: List[str]

    class Config:
        extra: 'allow'
        arbitrary_types_allowed = True


class ManifestNode(BaseNode, pydantic.BaseModel):
    """
    The node object

    Examples:

        Get a model node by name.

        >>> from artefacts import Project
        >>> project = Project()
        >>> model = project.get_model('customers')
        >>> model.config
        {'a': 1}
        >>> model.resource_type
        'model'

        You can also retrieve any type of node by its _unique_id_.

        >>> seed = project.get_node_by_id('seed.jaffle_shop.orders')
        >>> seed.children
        [<ModelNode orders>]
    """

    class Config:
        extra = 'allow'

    @property
    def project(self):
        return Project

    config: dict
    path: str
    original_file_path: str
    resource_type: str
    database: str
    unique_id: str
    depends_on: 'DependsOn'
    name: str
    alias: str
    tags: List[str]

    # We should make column values an attribute, which has methods for things like
    # "created" and "docs". Ie model.columns['user_id'].description
    columns: dict

    # We should rename this to "schema_name"
    db_schema: str = pydantic.Field(alias='schema')

    @classmethod
    def from_unique_id(cls, unique_id):
        return NodeReference(unique_id)

    # TODO: we can test that the model exists based on the catalog.json
    def exists(self):
        pass

    @property 
    def children(self):
        return self.project.manifest.child_map[self]

    @property
    def parents(self):
        return self.project.manifest.parent_map[self]

    @property
    def tests(self):
        results = []
        for node in self.children:
            if node.resource_type == 'test':
                results.append(node)
        return results

    @property
    def catalog(self):
        return self.project.catalog.nodes[self]


class CatalogNodeColumn(pydantic.BaseModel):
    type: str
    index: int
    name: str
    comment: Union[str, None]


class CatalogNode(BaseNode, pydantic.BaseModel):
    metadata: dict
    columns: Dict[str, CatalogNodeColumn]
    unique_id: Union[str, None]


class Manifest(pydantic.BaseModel):
    """
    Test Docs for the manifest class
    """

    class Config:
        arbitrary_types_allowed = True

    metadata: dict
    """
    dict: Some metadata about the manifest
    """

    nodes: Dict[NodeReference, ManifestNode]
    project: 'Project'
    child_map: Dict[NodeReference, List[NodeReference]]
    parent_map: Dict[NodeReference, List[NodeReference]]


class Catalog(pydantic.BaseModel):
    """
    Test Docs for the Catalog class
    """

    class Config:
        arbitrary_types_allowed = True

    metadata: dict
    nodes: Dict[NodeReference, CatalogNode]
    project: 'Project'

    # Note, when getting a KeyError using the nodes dict, it's likely caused by the model
    # not existing in the database yet. It can usually be fixed by using `dbt run`.


class Project(object):
    """
    Examples:

        After `dbt compile`ing your project, list all the models in the project.

        >>> from artefacts import Project
        >>> project = Project()
        >>> for model in project.models:
        ...     print(model.name)

    Attributes:

        manifest (Manifest): The project's compiled [`Manifest`][artefacts.models.Manifest], which includes
                             information about models, tests, sources, seeds, and other data about project.

        catalog (Catalog): The project's compiled [`Catalog`][artefacts.models.Catalog], which contains
                           information about the model's actual columns as defined in your data warehouse's
                           information_schema tables. Requires that `dbt docs generate` was ran before
                           initializing the object, ie before using `Project()`.
    """

    manifest: Manifest
    catalog: Catalog

    def __init__(self, target='./target'):
        Manifest.update_forward_refs()
        Catalog.update_forward_refs()

        with open(self.artifact_path(target, 'manifest'), 'r') as data:
            self.__class__.manifest = Manifest(**json.load(data), project=self)

        with open(self.artifact_path(target, 'catalog'), 'r') as data:
            self.__class__.catalog = Catalog(**json.load(data), project=self)

    def artifact_path(cls, target, name):
        return os.path.join(target, name + '.json')

    def get_model_by_path(self, path):
        for node_id, node in self.manifest.nodes.items():
            if node.resource_type == 'model' and node.original_file_path.endswith(str(path)):
                return node
        else:
            raise NodeNotFoundException

    def get_model_by_id(self, unique_id):
        try: 
            return self.manifest.nodes[unique_id]
        except KeyError:
            raise NodeNotFoundException

    def get_model_by_name(self, name):
        for model in self.models:
            if model.name == name:
                return model
        else:
            raise NodeNotFoundException

    @property
    def models(self):
        return [n for n in self.manifest.nodes if n.resource_type == 'model']

    @property
    def seeds(self):
        return [n for n in self.manifest.nodes if n.resource_type == 'seed']

    @property
    def tests(self):
        return [n for n in self.manifest.nodes if n.resource_type == 'test']