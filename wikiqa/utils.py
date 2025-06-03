"""
Utility classes for WikiQA
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class WikiPage:
    """Represents a Wikipedia page"""
    title: str
    content: str
    url: str
    revision_id: str
    last_modified: datetime
    
    @classmethod
    def from_wikipedia_page(cls, page):
        """Create a WikiPage instance from a wikipedia.Page object"""
        return cls(
            title=page.title,
            content=page.content,
            url=page.url,
            revision_id=page.revision_id,
            last_modified=datetime.now()  # Wikipedia API doesn't provide this
        )

@dataclass
class Entity:
    """Represents an extracted entity"""
    type: str
    value: str
    source: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entity':
        """Create an Entity instance from a dictionary"""
        return cls(
            type=data['type'],
            value=data['value'],
            source=data['source'],
            confidence=data.get('confidence', 1.0),
            metadata=data.get('metadata')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Entity instance to dictionary"""
        return {
            'type': self.type,
            'value': self.value,
            'source': self.source,
            'confidence': self.confidence,
            'metadata': self.metadata
        }

@dataclass
class Timeline:
    """Represents a chronological timeline"""
    events: List[Dict[str, Any]]
    source: str
    last_updated: str
    metadata: Dict[str, Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Timeline':
        """Create a Timeline instance from a dictionary"""
        return cls(
            events=data['events'],
            source=data['source'],
            last_updated=data['last_updated'],
            metadata=data.get('metadata')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Timeline instance to dictionary"""
        return {
            'events': self.events,
            'source': self.source,
            'last_updated': self.last_updated,
            'metadata': self.metadata
        }

@dataclass
class Citation:
    """Represents a citation or reference"""
    text: str
    source: str
    type: str
    metadata: Dict[str, Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Citation':
        """Create a Citation instance from a dictionary"""
        return cls(
            text=data['text'],
            source=data['source'],
            type=data['type'],
            metadata=data.get('metadata')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Citation instance to dictionary"""
        return {
            'text': self.text,
            'source': self.source,
            'type': self.type,
            'metadata': self.metadata
        }
    
    def format_mla(self) -> str:
        """Format citation in MLA style"""
        # Basic MLA format - can be expanded based on citation type
        return f"{self.text}. {self.source}."
    
    def format_apa(self) -> str:
        """Format citation in APA style"""
        # Basic APA format - can be expanded based on citation type
        return f"{self.text}. ({self.source})."
    
    def format_chicago(self) -> str:
        """Format citation in Chicago style"""
        # Basic Chicago format - can be expanded based on citation type
        return f"{self.text}. {self.source}." 