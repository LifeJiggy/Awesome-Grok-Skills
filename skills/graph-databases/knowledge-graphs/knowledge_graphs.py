"""
Knowledge Graphs Toolkit

Ontology design, RDF management, entity linking, graph embeddings,
and knowledge graph quality assurance.
"""

from __future__ import annotations

import math
import hashlib
import random
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import defaultdict
from abc import ABC, abstractmethod
import json as json

logger = __import__("logging").getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain Enums
# ---------------------------------------------------------------------------

class PropertyType(Enum):
    OBJECT = "object"       # Links entities to entities
    DATATYPE = "datatype"   # Links entities to literals
    ANNOTATION = "annotation"  # Metadata properties


class Cardinality(Enum):
    EXACTLY_ONE = auto()
    AT_MOST_ONE = auto()
    AT_LEAST_ONE = auto()
    ANY = auto()


class EmbeddingMethod(Enum):
    TRANSE = auto()
    NODE2VEC = auto()
    GCN = auto()
    GRAPHSAGE = auto()
    GAT = auto()


class SerializationFormat(Enum):
    TURTLE = "ttl"
    N_TRIPLES = "nt"
    JSON_LD = "jsonld"
    RDF_XML = "rdf"
    N3 = "n3"


class ValidationSeverity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    VIOLATION = auto()


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class OntologyClass:
    uri: str
    label: str
    parent: Optional[str] = None
    description: str = ""
    properties: list[str] = field(default_factory=list)
    equivalent_to: list[str] = field(default_factory=list)
    disjoint_with: list[str] = field(default_factory=list)

    @property
    def local_name(self) -> str:
        return self.uri.split("/")[-1].split("#")[-1]


@dataclass
class OntologyProperty:
    uri: str
    label: str
    property_type: PropertyType
    domain: str = ""
    range_type: str = ""
    cardinality: Cardinality = Cardinality.ANY
    is_transitive: bool = False
    is_symmetric: bool = False
    sub_property_of: Optional[str] = None

    @property
    def local_name(self) -> str:
        return self.uri.split("/")[-1].split("#")[-1]


@dataclass
class RDFTriple:
    subject: str
    predicate: str
    obj: str
    graph: str = ""
    is_literal: bool = False
    datatype: str = ""

    def to_turtle(self) -> str:
        if self.is_literal:
            return f"<{self.subject}> <{self.predicate}> \"{self.obj}\""
        return f"<{self.subject}> <{self.predicate}> <{self.obj}>"

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@id": self.subject,
            self.predicate: {"@id": self.obj} if not self.is_literal else {"@value": self.obj},
        }


@dataclass
class Entity:
    id: str
    label: str
    entity_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    embedding: Optional[list[float]] = None
    source: str = ""

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class LinkedEntity:
    mention: str
    entity_id: str
    confidence: float
    start_offset: int = 0
    end_offset: int = 0


@dataclass
class EmbeddingConfig:
    method: EmbeddingMethod
    dimensions: int = 128
    learning_rate: float = 0.01
    walk_length: int = 80
    num_walks: int = 10
    window_size: int = 10
    p: float = 1.0       # Node2Vec return parameter
    q: float = float("inf")  # Node2Vec in-out parameter
    epochs: int = 10


@dataclass
class ValidationViolation:
    severity: ValidationSeverity
    message: str
    entity_id: str = ""
    constraint: str = ""
    path: str = ""


@dataclass
class QualityReport:
    total_entities: int
    total_triples: int
    total_classes: int
    completeness: dict[str, float] = field(default_factory=dict)
    consistency: dict[str, float] = field(default_factory=dict)
    violations: list[ValidationViolation] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Ontology Builder
# ---------------------------------------------------------------------------

class OntologyBuilder:
    """Builds and validates OWL ontologies."""

    def __init__(self, base_uri: str = "http://example.org/") -> None:
        self._base_uri = base_uri
        self._classes: dict[str, OntologyClass] = {}
        self._properties: dict[str, OntologyProperty] = {}

    def add_class(self, label: str, parent: Optional[str] = None, **kwargs: Any) -> OntologyClass:
        uri = f"{self._base_uri}{label}"
        cls = OntologyClass(uri=uri, label=label, parent=parent, **kwargs)
        self._classes[uri] = cls
        if parent and parent in self._classes:
            self._classes[parent].properties.extend(cls.properties)
        return cls

    def add_property(self, label: str, prop_type: PropertyType,
                     domain: str = "", range_type: str = "", **kwargs: Any) -> OntologyProperty:
        uri = f"{self._base_uri}{label}"
        prop = OntologyProperty(uri=uri, label=label, property_type=prop_type,
                                domain=domain, range_type=range_type, **kwargs)
        self._properties[uri] = prop
        if domain and domain in self._classes:
            self._classes[domain].properties.append(uri)
        return prop

    def get_classes(self) -> list[OntologyClass]:
        return list(self._classes.values())

    def get_properties(self) -> list[OntologyProperty]:
        return list(self._properties.values())

    def validate_class_hierarchy(self) -> list[str]:
        errors: list[str] = []
        for cls in self._classes.values():
            if cls.parent and cls.parent not in self._classes:
                errors.append(f"Class '{cls.label}' references unknown parent '{cls.parent}'")
            if cls.uri in cls.disjoint_with:
                errors.append(f"Class '{cls.label}' is disjoint with itself")
        return errors

    def to_turtle(self) -> str:
        lines = [
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
            "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
            "",
        ]
        for cls in self._classes.values():
            lines.append(f"<{cls.uri}> rdf:type owl:Class ;")
            if cls.parent:
                lines.append(f"    rdfs:subClassOf <{self._classes[cls.parent].uri if cls.parent in self._classes else cls.parent}> ;")
            if cls.description:
                lines.append(f'    rdfs:label "{cls.description}"@en ;')
            lines[-1] = lines[-1].rstrip(" ;") + " ."
            lines.append("")

        for prop in self._properties.values():
            prop_class = "owl:ObjectProperty" if prop.property_type == PropertyType.OBJECT else "owl:DatatypeProperty"
            lines.append(f"<{prop.uri}> rdf:type {prop_class} ;")
            if prop.domain:
                lines.append(f"    rdfs:domain <{prop.domain}> ;")
            if prop.range_type:
                lines.append(f"    rdfs:range <{prop.range_type}> ;")
            if prop.is_transitive:
                lines.append(f"    rdf:type owl:TransitiveProperty ;")
            lines[-1] = lines[-1].rstrip(" ;") + " ."
            lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# RDF Store
# ---------------------------------------------------------------------------

class RDFStore:
    """In-memory RDF triple store with SPARQL-like query support."""

    def __init__(self) -> None:
        self._triples: list[RDFTriple] = []
        self._index_spo: dict[tuple[str, str], list[str]] = defaultdict(list)
        self._index_pos: dict[tuple[str, str], list[str]] = defaultdict(list)
        self._index_osp: dict[tuple[str, str], list[str]] = defaultdict(list)
        self._namespaces: dict[str, str] = {}

    def add(self, triple: RDFTriple) -> None:
        self._triples.append(triple)
        self._index_spo[(triple.subject, triple.predicate)].append(triple.obj)
        self._index_pos[(triple.predicate, triple.obj)].append(triple.subject)
        self._index_osp[(triple.obj, triple.subject)].append(triple.predicate)

    def add_triple(self, subject: str, predicate: str, obj: str, **kwargs: Any) -> None:
        self.add(RDFTriple(subject=subject, predicate=predicate, obj=obj, **kwargs))

    def size(self) -> int:
        return len(self._triples)

    def query_pattern(self, subject: Optional[str] = None, predicate: Optional[str] = None,
                      obj: Optional[str] = None) -> list[RDFTriple]:
        results = self._triples
        if subject:
            results = [t for t in results if t.subject == subject]
        if predicate:
            results = [t for t in results if t.predicate == predicate]
        if obj:
            results = [t for t in results if t.obj == obj]
        return results

    def subjects(self) -> set[str]:
        return {t.subject for t in self._triples}

    def predicates(self) -> set[str]:
        return {t.predicate for t in self._triples}

    def objects(self) -> set[str]:
        return {t.obj for t in self._triples}

    def to_jsonld(self) -> list[dict[str, Any]]:
        by_subject: dict[str, dict[str, list[Any]]] = defaultdict(lambda: defaultdict(list))
        for triple in self._triples:
            if triple.is_literal:
                by_subject[triple.subject][triple.predicate].append(triple.obj)
            else:
                by_subject[triple.subject][triple.predicate].append({"@id": triple.obj})
        result: list[dict[str, Any]] = []
        for subj, preds in by_subject.items():
            node: dict[str, Any] = {"@id": subj}
            for pred, objects in preds.items():
                if len(objects) == 1:
                    node[pred] = objects[0]
                else:
                    node[pred] = objects
            result.append(node)
        return result


# ---------------------------------------------------------------------------
# Entity Linker
# ---------------------------------------------------------------------------

class EntityLinker:
    """Links text mentions to knowledge graph entities."""

    def __init__(self, store: RDFStore) -> None:
        self._store = store
        self._entity_index: dict[str, list[Entity]] = defaultdict(list)
        self._type_index: dict[str, list[str]] = defaultdict(list)

    def index_entity(self, entity: Entity) -> None:
        tokens = entity.label.lower().split()
        for token in tokens:
            self._entity_index[token].append(entity)
        self._type_index[entity.entity_type].append(entity.id)

    def candidate_generation(self, mention: str, entity_type: Optional[str] = None) -> list[Entity]:
        tokens = mention.lower().split()
        candidates: list[Entity] = []
        seen_ids: set[str] = set()
        for token in tokens:
            for entity in self._entity_index.get(token, []):
                if entity.id not in seen_ids:
                    if entity_type is None or entity.entity_type == entity_type:
                        candidates.append(entity)
                        seen_ids.add(entity.id)
        return candidates

    def score_candidate(self, mention: str, entity: Entity) -> float:
        mention_lower = mention.lower()
        label_lower = entity.label.lower()
        if mention_lower == label_lower:
            return 1.0
        if mention_lower in label_lower or label_lower in mention_lower:
            return 0.7
        mention_tokens = set(mention_lower.split())
        label_tokens = set(label_lower.split())
        if mention_tokens and label_tokens:
            jaccard = len(mention_tokens & label_tokens) / len(mention_tokens | label_tokens)
            return jaccard * 0.6
        return 0.1

    def link(self, mention: str, entity_type: Optional[str] = None,
             threshold: float = 0.3) -> Optional[LinkedEntity]:
        candidates = self.candidate_generation(mention, entity_type)
        if not candidates:
            return None
        scored = [(c, self.score_candidate(mention, c)) for c in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        best_entity, best_score = scored[0]
        if best_score < threshold:
            return None
        return LinkedEntity(
            mention=mention, entity_id=best_entity.id,
            confidence=best_score,
        )

    def link_batch(self, mentions: list[str], entity_type: Optional[str] = None,
                   threshold: float = 0.3) -> list[Optional[LinkedEntity]]:
        return [self.link(m, entity_type, threshold) for m in mentions]


# ---------------------------------------------------------------------------
# Graph Embedder
# ---------------------------------------------------------------------------

class GraphEmbedder:
    """Learns vector embeddings for graph nodes."""

    def __init__(self, config: Optional[EmbeddingConfig] = None) -> None:
        self._config = config or EmbeddingConfig(method=EmbeddingMethod.NODE2VEC)
        self._embeddings: dict[str, list[float]] = {}
        self._adjacency: dict[str, list[str]] = defaultdict(list)

    def add_edge(self, source: str, target: str) -> None:
        self._adjacency[source].append(target)
        self._adjacency[target].append(source)

    def _random_walk(self, start: str, length: int) -> list[str]:
        walk = [start]
        current = start
        for _ in range(length - 1):
            neighbors = self._adjacency.get(current, [])
            if not neighbors:
                break
            current = random.choice(neighbors)
            walk.append(current)
        return walk

    def _node2vec_walk(self, start: str, length: int) -> list[str]:
        walk = [start]
        prev = None
        current = start
        for _ in range(length - 1):
            neighbors = self._adjacency.get(current, [])
            if not neighbors:
                break
            if prev is None:
                next_node = random.choice(neighbors)
            else:
                probs: list[tuple[str, float]] = []
                for neighbor in neighbors:
                    if neighbor == prev:
                        weight = 1.0 / self._config.p
                    elif neighbor in self._adjacency.get(prev, []):
                        weight = 1.0
                    else:
                        weight = 1.0 / self._config.q
                    probs.append((neighbor, weight))
                total = sum(w for _, w in probs)
                r = random.random() * total
                cumulative = 0.0
                next_node = neighbors[0]
                for neighbor, weight in probs:
                    cumulative += weight
                    if cumulative >= r:
                        next_node = neighbor
                        break
            prev = current
            current = next_node
            walk.append(current)
        return walk

    def fit(self, nodes: list[str]) -> dict[str, list[float]]:
        all_walks: list[list[str]] = []
        for _ in range(self._config.num_walks):
            for node in nodes:
                if self._config.method == EmbeddingMethod.NODE2VEC:
                    walk = self._node2vec_walk(node, self._config.walk_length)
                else:
                    walk = self._random_walk(node, self._config.walk_length)
                all_walks.append(walk)

        vocab = {node: i for i, node in enumerate(nodes)}
        dim = self._config.dimensions
        vectors = {node: [random.gauss(0, 0.1) for _ in range(dim)] for node in nodes}

        for epoch in range(self._config.epochs):
            for walk in all_walks:
                for i, center in enumerate(walk):
                    window = walk[max(0, i - self._config.window_size):i + self._config.window_size + 1]
                    for context in window:
                        if context != center:
                            ci = vocab.get(center)
                            cj = vocab.get(context)
                            if ci is not None and cj is not None:
                                error = [vectors[context][d] - vectors[center][d] for d in range(dim)]
                                for d in range(dim):
                                    vectors[center][d] -= self._config.learning_rate * error[d]
                                    vectors[context][d] -= self._config.learning_rate * error[d]

        self._embeddings = vectors
        return vectors

    def get_embedding(self, node: str) -> Optional[list[float]]:
        return self._embeddings.get(node)

    def similarity(self, node_a: str, node_b: str) -> float:
        emb_a = self._embeddings.get(node_a)
        emb_b = self._embeddings.get(node_b)
        if not emb_a or not emb_b:
            return 0.0
        dot = sum(a * b for a, b in zip(emb_a, emb_b))
        norm_a = math.sqrt(sum(a ** 2 for a in emb_a))
        norm_b = math.sqrt(sum(b ** 2 for b in emb_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def nearest_neighbors(self, node: str, k: int = 5) -> list[tuple[str, float]]:
        scores = []
        for other in self._embeddings:
            if other != node:
                scores.append((other, self.similarity(node, other)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]


# ---------------------------------------------------------------------------
# Quality Assessor
# ---------------------------------------------------------------------------

class KnowledgeGraphQualityAssessor:
    """Evaluates knowledge graph quality and completeness."""

    def __init__(self, store: RDFStore, ontology: OntologyBuilder) -> None:
        self._store = store
        self._ontology = ontology

    def check_orphan_entities(self) -> list[str]:
        orphans: list[str] = []
        for subj in self._store.subjects():
            triples = self._store.query_pattern(subject=subj)
            if len(triples) <= 1:
                orphans.append(subj)
        return orphans

    def check_missing_types(self) -> list[str]:
        typed = {t.subject for t in self._store.query_pattern(predicate="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")}
        all_subjects = self._store.subjects()
        return list(all_subjects - typed)

    def check_property_completeness(self, property_uri: str, class_uri: str) -> float:
        class_instances = {t.subject for t in self._store.query_pattern(
            predicate="http://www.w3.org/1999/02/22-rdf-syntax-ns#type", obj=class_uri
        )}
        if not class_instances:
            return 1.0
        with_property = {t.subject for t in self._store.query_pattern(predicate=property_uri)}
        return len(class_instances & with_property) / len(class_instances)

    def compute_completeness(self) -> dict[str, float]:
        completeness: dict[str, float] = {}
        for cls in self._ontology.get_classes():
            for prop_uri in cls.properties:
                key = f"{cls.local_name}.{self._ontology._properties[prop_uri].local_name if prop_uri in self._ontology._properties else prop_uri}"
                completeness[key] = self.check_property_completeness(prop_uri, cls.uri)
        return completeness

    def validate(self) -> list[ValidationViolation]:
        violations: list[ValidationViolation] = []
        orphans = self.check_orphan_entities()
        for orphan in orphans:
            violations.append(ValidationViolation(
                severity=ValidationSeverity.WARNING,
                message=f"Orphan entity with no relationships: {orphan}",
                entity_id=orphan,
            ))
        missing_types = self.check_missing_types()
        for mt in missing_types:
            violations.append(ValidationViolation(
                severity=ValidationSeverity.ERROR,
                message=f"Entity without type declaration: {mt}",
                entity_id=mt,
            ))
        return violations

    def full_report(self) -> QualityReport:
        return QualityReport(
            total_entities=self._store.size(),
            total_triples=self._store.size(),
            total_classes=len(self._ontology.get_classes()),
            completeness=self.compute_completeness(),
            violations=self.validate(),
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("KNOWLEDGE GRAPHS TOOLKIT DEMO")
    print("=" * 70)

    # Ontology Design
    print("\n--- Ontology Design ---")
    ontology = OntologyBuilder(base_uri="http://example.org/schema/")
    person_cls = ontology.add_class("Person", description="A human being")
    org_cls = ontology.add_class("Organization", description="A group entity")
    event_cls = ontology.add_class("Event")
    ontology.add_class("WorkEvent", parent="http://example.org/schema/Event")

    knows_prop = ontology.add_property("knows", PropertyType.OBJECT, domain="http://example.org/schema/Person", range_type="http://schema.org/Person")
    works_at_prop = ontology.add_property("worksAt", PropertyType.OBJECT, domain="http://example.org/schema/Person")
    name_prop = ontology.add_property("name", PropertyType.DATATYPE, domain="http://example.org/schema/Person")
    email_prop = ontology.add_property("email", PropertyType.DATATYPE, domain="http://example.org/schema/Person", cardinality=Cardinality.EXACTLY_ONE)

    errors = ontology.validate_class_hierarchy()
    print(f"  Classes: {[c.local_name for c in ontology.get_classes()]}")
    print(f"  Properties: {[p.local_name for p in ontology.get_properties()]}")
    print(f"  Validation errors: {errors}")
    print(f"  Turtle output:\n{ontology.to_turtle()[:500]}...")

    # RDF Store
    print("\n--- RDF Store ---")
    store = RDFStore()
    store.add_triple("http://ex.org/alice", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://ex.org/Person")
    store.add_triple("http://ex.org/alice", "http://ex.org/name", "Alice Smith", is_literal=True)
    store.add_triple("http://ex.org/alice", "http://ex.org/email", "alice@example.com", is_literal=True)
    store.add_triple("http://ex.org/alice", "http://ex.org/knows", "http://ex.org/bob")
    store.add_triple("http://ex.org/bob", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://ex.org/Person")
    store.add_triple("http://ex.org/bob", "http://ex.org/name", "Bob Jones", is_literal=True)
    store.add_triple("http://ex.org/bob", "http://ex.org/worksAt", "http://ex.org/acme")
    store.add_triple("http://ex.org/acme", "http://ex.org/name", "Acme Corp", is_literal=True)
    print(f"  Triples stored: {store.size()}")
    print(f"  Subjects: {store.subjects()}")
    print(f"  Query (predicate=knows): {[(t.subject, t.obj) for t in store.query_pattern(predicate='http://ex.org/knows')]}")
    jsonld = store.to_jsonld()
    print(f"  JSON-LD nodes: {len(jsonld)}")

    # Entity Linking
    print("\n--- Entity Linking ---")
    linker = EntityLinker(store)
    alice = Entity("http://ex.org/alice", "Alice Smith", "Person")
    bob = Entity("http://ex.org/bob", "Bob Jones", "Person")
    acme = Entity("http://ex.org/acme", "Acme Corp", "Organization")
    linker.index_entity(alice)
    linker.index_entity(bob)
    linker.index_entity(acme)

    result1 = linker.link("Alice")
    result2 = linker.link("Acme Corp")
    result3 = linker.link("Unknown Person")
    print(f"  Link 'Alice': {result1}")
    print(f"  Link 'Acme Corp': {result2}")
    print(f"  Link 'Unknown Person': {result3}")

    batch_results = linker.link_batch(["Alice", "Bob", "Acme"], entity_type="Person")
    print(f"  Batch links: {[(r.mention, r.entity_id, r.confidence) if r else None for r in batch_results]}")

    # Graph Embeddings
    print("\n--- Graph Embeddings ---")
    embedder = GraphEmbedder(EmbeddingConfig(method=EmbeddingMethod.NODE2VEC, dimensions=16, num_walks=5, epochs=5))
    embedder.add_edge("alice", "bob")
    embedder.add_edge("alice", "carol")
    embedder.add_edge("bob", "carol")
    embedder.add_edge("bob", "dave")
    embedder.add_edge("carol", "eve")
    embedder.add_edge("dave", "eve")
    embedder.add_edge("eve", "frank")

    vectors = embedder.fit(["alice", "bob", "carol", "dave", "eve", "frank"])
    print(f"  Embedding dimensions: {len(vectors['alice'])}")
    print(f"  alice<->bob similarity: {embedder.similarity('alice', 'bob'):.4f}")
    print(f"  alice<->frank similarity: {embedder.similarity('alice', 'frank'):.4f}")
    neighbors = embedder.nearest_neighbors("alice", k=3)
    print(f"  Alice nearest neighbors: {neighbors}")

    # Quality Assessment
    print("\n--- Quality Assessment ---")
    assessor = KnowledgeGraphQualityAssessor(store, ontology)
    report = assessor.full_report()
    print(f"  Total triples: {report.total_triples}")
    print(f"  Orphan entities: {[v.entity_id for v in report.violations if 'Orphan' in v.message]}")
    print(f"  Missing types: {[v.entity_id for v in report.violations if 'without type' in v.message]}")
    print(f"  Completeness: {report.completeness}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")


if __name__ == "__main__":
    main()
