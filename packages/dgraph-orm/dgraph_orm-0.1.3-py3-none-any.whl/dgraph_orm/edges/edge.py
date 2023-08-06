"""ATTEMPT TO SIMPLIFY, CAN IGNORE"""
from __future__ import annotations
import typing as T
from pydantic import BaseModel


class Node(BaseModel):
    def query(
        self, params: QueryParams = None, edges: Edges = None
    ) -> T.List[NodeType]:
        print(f"{params=}, {edges=}")
        return [NodeType()]

    def get(self, params: GetParams) -> T.Optional[NodeType]:
        pass


NodeType = T.TypeVar("NodeType")
QueryParams = T.TypeVar("QueryParams")
GetParams = T.TypeVar("GetParams")
Edges = T.TypeVar("Edges")


class Edge(BaseModel, T.Generic[NodeType, QueryParams, GetParams, Edges]):
    _query_params: QueryParams
    _get_params: GetParams
    _edges: Edges

    @property
    def query_params(self) -> QueryParams:
        return self._query_params

    @property
    def _get_params(self) -> QueryParams:
        return self._query_params

    @property
    def _edges(self) -> QueryParams:
        return self._query_params

    def query(
        self, params: QueryParams = None, edges: Edges = None
    ) -> T.List[NodeType]:
        print(f"{params=}, {edges=}")
        return [NodeType()]

    def get(self, params: GetParams) -> T.Optional[NodeType]:
        pass


student = Student.query(edges=Edges(taught_by=Teacher.get()))
