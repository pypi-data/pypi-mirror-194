from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict

from marshmallow_dataclass import class_schema

from semantha_sdk.model.reference import Reference
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema
from semantha_sdk.model.sentence import Sentence


@dataclass(frozen=True)
class Paragraph(SemanthaModelEntity):
    id: str
    type: str
    text: str
    sentences: Optional[List[Sentence]]
    document_name: Optional[str]
    references: Optional[List[Reference]]
    context: Optional[Dict[str, str]]
    comment: Optional[str]


ParagraphSchema = class_schema(Paragraph, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class PatchParagraph(SemanthaModelEntity):
    id: Optional[str]
    type: Optional[str]
    text: Optional[str]
    sentences: Optional[List[Sentence]]
    document_name: Optional[Optional[str]]
    references: Optional[List[Reference]]
    context: Optional[Dict[str, str]]
    comment: Optional[str]
