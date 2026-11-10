'use strict';

// ---------------------------------------------------------------------------
// Gene Schema — single source of truth for the Gene object shape.
// All modules that create or consume Gene objects should use createGene() and
// validateGene() rather than assuming field presence inline.
// ---------------------------------------------------------------------------

const VALID_CATEGORIES = ['repair', 'optimize', 'innovate', 'explore'];

// EvoX agent-core enums consumed via the gene → router/tool-gate
// pipeline (`crates/evox-evo-session/src/lifecycle.rs:345-388`). Keep
// these strings exact — the Rust side does case-sensitive matching.
const VALID_ROUTING_TIERS = ['cheap', 'mid', 'expensive'];
const VALID_REASONING_LEVELS = ['off', 'low', 'medium', 'high'];
const VALID_TOOL_POLICY_SEVERITIES = ['warn', 'block'];

const GENE_DEFAULTS = {
  type: 'Gene',
  id: null,
  category: 'innovate',
  signals_match: [],
  strategy: [],
  validation: [],
  constraints: {
    max_files: 20,
    forbidden_paths: ['.git', 'node_modules'],
  },
  preconditions: [],
  summary: '',
  schema_version: '1.6.0',
  epigenetic_marks: [],
  learning_history: [],
  anti_patterns: [],
  // Optional EvoX-side hints. Null = "no opinion, let the router /
  // tool dispatcher take its historical fast path". Genes that
  // genuinely benefit from cheap-tier classification or restricted
  // tools opt in by setting these to a non-null object.
  routing_hint: null,
  tool_policy: null,
};

// createGene: merge partial with defaults and normalize array/object fields.
// Safe to call with a fully-formed Gene (idempotent).
function createGene(partial) {
  const g = Object.assign({}, GENE_DEFAULTS, partial);

  // Always create fresh array copies — never hold references to GENE_DEFAULTS arrays
  // or to partial's arrays, so downstream .push() calls cannot contaminate other genes.
  g.signals_match    = Array.isArray(g.signals_match)    ? g.signals_match.slice()    : [];
  g.strategy         = Array.isArray(g.strategy)         ? g.strategy.slice()         : [];
  g.validation       = Array.isArray(g.validation)       ? g.validation.slice()       : [];
  g.preconditions    = Array.isArray(g.preconditions)    ? g.preconditions.slice()    : [];
  g.epigenetic_marks = Array.isArray(g.epigenetic_marks) ? g.epigenetic_marks.slice() : [];
  g.learning_history = Array.isArray(g.learning_history) ? g.learning_history.slice() : [];
  g.anti_patterns    = Array.isArray(g.anti_patterns)    ? g.anti_patterns.slice()    : [];

  // Normalize constraints
  if (!g.constraints || typeof g.constraints !== 'object') {
    g.constraints = Object.assign({}, GENE_DEFAULTS.constraints);
  } else {
    g.constraints = Object.assign({}, GENE_DEFAULTS.constraints, g.constraints);
  }
  if (!Array.isArray(g.constraints.forbidden_paths) || g.constraints.forbidden_paths.length === 0) {
    g.constraints.forbidden_paths = ['.git', 'node_modules'];
  } else {
    g.constraints.forbidden_paths = g.constraints.forbidden_paths.slice();
  }
  if (!g.constraints.max_files || typeof g.constraints.max_files !== 'number') {
    g.constraints.max_files = GENE_DEFAULTS.constraints.max_files;
  }

  // Normalize category
  if (!g.category || !VALID_CATEGORIES.includes(g.category)) {
    g.category = GENE_DEFAULTS.category;
  }

  // Normalize string fields
  if (typeof g.summary !== 'string')        g.summary = '';
  if (typeof g.schema_version !== 'string') g.schema_version = GENE_DEFAULTS.schema_version;

  // Normalize optional routing_hint / tool_policy. The EvoX agent-core
  // side (`crates/evox-evo-session/src/lifecycle.rs`) treats absent
  // *or* empty hints as "no opinion" via `GeneRoutingHint::is_empty()`,
  // so dropping malformed fragments to `null` is the safer default —
  // a partial object would fail the strict tier-string match on the
  // Rust side and silently route as if no hint existed.
  g.routing_hint = normalizeRoutingHint(g.routing_hint);
  g.tool_policy  = normalizeToolPolicy(g.tool_policy);

  return g;
}

function normalizeRoutingHint(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const out = {};
  if (raw.tier && VALID_ROUTING_TIERS.includes(String(raw.tier))) {
    out.tier = String(raw.tier);
  }
  if (raw.reasoning_level && VALID_REASONING_LEVELS.includes(String(raw.reasoning_level))) {
    out.reasoning_level = String(raw.reasoning_level);
  }
  return Object.keys(out).length > 0 ? out : null;
}

function normalizeToolPolicy(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const out = {};
  // Filter falsy entries first, then only keep the field if anything
  // survives. A raw input like { allow_only: ['', ''] } would otherwise
  // emit `allow_only: []` here; on the Rust executor gate
  // (`crates/evox-agent-core/src/types.rs::ToolGate`) an empty
  // `allow_only` means "allow zero tools" and blocks every tool call.
  if (Array.isArray(raw.allow_only)) {
    const cleaned = raw.allow_only.map(String).filter(Boolean);
    if (cleaned.length > 0) out.allow_only = cleaned;
  }
  if (Array.isArray(raw.deny)) {
    const cleaned = raw.deny.map(String).filter(Boolean);
    if (cleaned.length > 0) out.deny = cleaned;
  }
  // severity defaults to 'warn' when omitted but a list is present —
  // matches `GeneToolPolicy::default_severity()` on the Rust side.
  const hasList = !!(out.allow_only || out.deny);
  if (hasList) {
    out.severity = VALID_TOOL_POLICY_SEVERITIES.includes(String(raw.severity))
      ? String(raw.severity)
      : 'warn';
  }
  return hasList ? out : null;
}

// validateGene: throw if required fields are missing or malformed.
// Use before broadcasting/publishing a Gene to the Hub or writing to disk.
function validateGene(g) {
  if (!g || typeof g !== 'object')          throw new Error('Gene must be an object');
  if (g.type !== 'Gene')                    throw new Error('Gene.type must be "Gene", got: ' + g.type);
  if (!g.id || typeof g.id !== 'string')    throw new Error('Gene.id is required and must be a string');
  if (!VALID_CATEGORIES.includes(g.category))
                                            throw new Error('Gene.category must be one of: ' + VALID_CATEGORIES.join(', ') + ', got: ' + g.category);
  if (!Array.isArray(g.signals_match))      throw new Error('Gene.signals_match must be an array');
  if (g.trigger !== undefined && g.trigger !== null && typeof g.trigger !== 'string')
                                            throw new Error('Gene.trigger must be a string');
  if (!Array.isArray(g.strategy))           throw new Error('Gene.strategy must be an array');
  return true;
}

module.exports = {
  createGene,
  validateGene,
  GENE_DEFAULTS,
  VALID_CATEGORIES,
  VALID_ROUTING_TIERS,
  VALID_REASONING_LEVELS,
  VALID_TOOL_POLICY_SEVERITIES,
};
