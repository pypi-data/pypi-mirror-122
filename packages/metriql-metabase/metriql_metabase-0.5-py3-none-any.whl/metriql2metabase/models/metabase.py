from dataclasses import dataclass, field

from typing import Sequence, Optional

@dataclass
class MetabaseColumn:
    name: str
    description: str = ""
    label: str = ""
    semantic_type: Optional[str] = None
    visibility_type: Optional[str] = None


@dataclass
class MetabaseMetric:
    name: str
    label: str = ""
    description: str = ""


@dataclass
class MetabaseModel:
    name: str
    schema: str
    description: str = ""
    label: str = ""
    columns: Sequence[MetabaseColumn] = field(default_factory=list)
    metrics: Sequence[MetabaseMetric] = field(default_factory=list)
    hidden: bool = False

