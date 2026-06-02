/** JSON-like config value accepted by parser config metadata. */
export type ConfigValue = string | number | boolean | null | ConfigObject | ConfigValue[];

/** Object-shaped parser config defaults. */
export interface ConfigObject {
  [key: string]: ConfigValue;
}

/** Immutable runtime/task/thread defaults selected by Control Plane and Agent. */
export interface RuntimeInfo {
  parser_alias: string;
  task_alias: string;
  run_id: number | null;
  task_id: number | null;
  max_concurrent_tasks: number;
  thread_config_alias: string | null;
  request_delay_sec: number;
  http_transport_mode: string;
  request_timeout_sec: number;
  request_max_retries: number;
}

/** Structured logger facade. Agent owns shipping, retention, and visibility. */
export interface Logger {
  /** Write diagnostic details for troubleshooting without changing parser flow. */
  debug(message: string, extra?: unknown): Promise<void>;
  /** Write a normal progress message to run logs. */
  info(message: string, extra?: unknown): Promise<void>;
  /** Write a warning while allowing the current item or run to continue. */
  warn(message: string, extra?: unknown): Promise<void>;
  /** Alias for warn(), kept for parser authors who prefer Python-style naming. */
  warning(message: string, extra?: unknown): Promise<void>;
  /** Write an error log entry; throw a parser error separately to fail work. */
  error(message: string, extra?: unknown): Promise<void>;
}

/** Custom metric facade. Values are sent to platform-owned metrics ingest. */
export interface MetricsFacade {
  /**
   * Emit one custom parser metric sample.
   * @example
   * await this.metrics.emit('items_seen', 1, { source: 'catalog' });
   */
  emit(name: string, value?: number, labels?: Record<string, string>): Promise<void>;
}

/** Queue facade for follow-up work items; broker details remain internal. */
export interface QueryFacade {
  /** Enqueue one follow-up item for this parser. */
  add(item: unknown): Promise<void>;
  /** Alias for add(), useful when parser code models queue writes as pushes. */
  push(item: unknown): Promise<void>;
}

/** Runtime reservation for one Egress member. */
export interface EgressLease {
  lease_id: string;
  pool_key?: string | null;
  item_type?: string | null;
  endpoint?: string | null;
  endpoint_url?: string | null;
  transport_mode?: string | null;
  [key: string]: unknown;
}

/** Selector for exact lease, transport mode, or Egress member type. */
export interface EgressSelector {
  leaseId?: string | null;
  lease_id?: string | null;
  httpMode?: string | null;
  http_mode?: string | null;
  itemType?: string | null;
  item_type?: string | null;
  reason?: string | null;
  ttlSec?: number | null;
  ttl_sec?: number | null;
}

/** Parser-facing Egress operations. Agent owns the actual lease lifecycle. */
export interface EgressFacade {
  /** Return the current matching lease, if one is already reserved. */
  current(selector?: EgressSelector): Promise<EgressLease | null>;
  /** Release a lease back to the pool. */
  release(selector?: EgressSelector): Promise<void>;
  /**
   * Reserve the next matching Egress member.
   * @example
   * const lease = await this.egress.next({ httpMode: this.runtime.http_transport_mode });
   */
  next(selector?: EgressSelector): Promise<EgressLease>;
  /** Mark a matching Egress member as temporarily unusable. */
  ban(selector?: EgressSelector): Promise<EgressLease | null>;
}

/** Cookie/session facade where the runtime provides it. */
export interface CookieFacade {
  /** Read all cookies from the active runtime session. */
  getAll(): Promise<unknown[]>;
  /** Replace all cookies in the active runtime session. */
  setAll(cookies: unknown[]): Promise<void>;
  /** Set one cookie value for a host/path/name tuple. */
  set(host: string, path: string, name: string, value: string): Promise<void>;
}

/** Output workspace file helpers. Paths are resolved by the runtime host. */
export interface FilesFacade {
  /** Create a directory below the run output workspace. */
  mkdir(path: string): Promise<unknown>;
  /** Remove a directory tree below the run output workspace. */
  removeTree(path: string): Promise<unknown>;
  /**
   * Write text below the run output workspace.
   * @example
   * await this.files.writeText('pages/item.html', html);
   */
  writeText(path: string, data: string, encoding?: string): Promise<{ bytes: number }>;
  /** Write bytes below the run output workspace. */
  writeBytes(path: string, data: Uint8Array): Promise<{ bytes: number }>;
}

/** Durable dataset reference returned after publication. */
export interface DatasetRef {
  id: number;
  name: string;
  artifact_blob_id?: number | null;
  sha256: string;
  size_bytes: number;
  content_type?: string | null;
  source_run_id?: number | null;
  source_task_alias?: string | null;
  source_key?: string | null;
  metadata: Record<string, unknown>;
  created_at?: string | null;
}

/** Run-local output handle for a file already written in the workspace. */
export interface LocalOutputHandle {
  id: number;
  run_id: number;
  handle: string;
  relative_path: string;
  output_kind: string;
  task_alias?: string | null;
  agent_id?: string | null;
  content_type?: string | null;
  size_bytes?: number | null;
  sha256?: string | null;
  published_dataset_id?: number | null;
  metadata: Record<string, unknown>;
}

/** Options for publishing a durable dataset. Use path for large payloads. */
export interface PublishDatasetOptions {
  path?: string;
  content?: string | Uint8Array;
  contentType?: string | null;
  metadata?: Record<string, unknown>;
}

/** Options for registering an output already written under the workspace. */
export interface RegisterOutputOptions {
  outputKind?: string;
  contentType?: string | null;
  metadata?: Record<string, unknown>;
}

/** Asset/output facade. Control Plane owns storage and access checks. */
export interface AssetsFacade {
  /** Read a sensitive asset as bytes through the runtime host. */
  readSensitiveBytes(assetId: number): Promise<Uint8Array>;
  /** Read a sensitive asset as decoded text through the runtime host. */
  readSensitiveText(assetId: number, encoding?: string): Promise<string>;
  /**
   * Publish content or a workspace file as a durable dataset.
   * @example
   * await this.assets.publishDataset('raw-html', { path: 'pages/item.html', contentType: 'text/html' });
   */
  publishDataset(name: string, options?: PublishDatasetOptions): Promise<DatasetRef>;
  /** Register a file already written in the workspace as a run-local output. */
  registerOutput(handle: string, path: string, options?: RegisterOutputOptions): Promise<LocalOutputHandle>;
}

/** HTTP response body exposed as bytes with a string conversion helper. */
export type ResponseBody = Uint8Array & {
  /** Decode the byte body using the requested encoding. */
  toString(encoding?: string): string;
};

/** Agent-executed HTTP response. */
export interface SdkResponse {
  ok: boolean;
  status: number;
  headers: Record<string, unknown>;
  body: ResponseBody;
  text: string;
  retries: number;
  elapsedMs: number;
  elapsed_ms: number;
  errorCode: string | null;
  error_code: string | null;
  egress: unknown | null;
  transportMode: string | null;
  transport_mode: string | null;
  /** Decode the response body as JSON using the runtime SDK parser. */
  json(): unknown;
}

/** Response validator used to replace default 200..399 success policy. */
export type ResponseValidator = (response: SdkResponse) => boolean | Promise<boolean>;

/** Per-request overrides; Thread Config still owns default policy. */
export interface RequestOptions {
  headers?: Record<string, string>;
  validateResponse?: ResponseValidator | ResponseValidator[];
  allowStatuses?: Array<number | string>;
  retries?: number;
  retryDelaySec?: number;
  timeout?: number;
  browser?: boolean;
  httpMode?: string;
  browserProfile?: string;
  body?: unknown;
}

/** Low-level request shape for BaseParser.request. */
export interface SdkRequest {
  method: string;
  url: string;
  params?: Record<string, unknown>;
  query?: Record<string, unknown>;
  body?: unknown;
  options?: RequestOptions;
}

/** Queue item wrapper passed to JavaScript parsers. */
export interface ParseSet {
  query: unknown;
}

/** Base class for JavaScript parsers. Runtime operations call the Agent host. */
export class BaseParser<TConfig extends ConfigObject = ConfigObject> {
  static parserAlias?: string;
  static alias?: string;
  static Config: ParserConfig;

  conf: TConfig;
  runtime: RuntimeInfo;
  logger: Logger;
  query: QueryFacade;
  queue: QueryFacade;
  egress: EgressFacade;
  cookies: CookieFacade;
  metrics: MetricsFacade;
  files: FilesFacade;
  assets: AssetsFacade;
  threadId: string;

  /** Create a parser bound to a runtime host; parser code normally relies on the platform to call this. */
  constructor(host?: unknown);
  /** Run once before parser work starts. */
  init(): void | Promise<void>;
  /** Run once after parser work finishes or aborts. */
  destroy(): void | Promise<void>;
  /** Run before a worker thread starts processing items. */
  initThread(): void | Promise<void>;
  /** Run after a worker thread stops processing items. */
  destroyThread(): void | Promise<void>;
  /**
   * Handle one queue item and optionally update the result object.
   * @example
   * async parse(set, results) {
   *   const response = await this.get(String(set.query));
   *   results.item = response.json();
   *   return results;
   * }
   */
  parse(set: ParseSet, results: Record<string, unknown>): unknown | Promise<unknown>;
  /** Execute one HTTP request through the Agent host. */
  request(request: SdkRequest): Promise<SdkResponse>;
  /**
   * Execute an HTTP GET through the Agent host.
   * @example
   * const response = await this.get('https://example.test/items', { page: 1 });
   */
  get(url: string, params?: Record<string, unknown>, options?: RequestOptions): Promise<SdkResponse>;
  /** Execute an HTTP POST through the Agent host. */
  post(
    url: string,
    body?: unknown,
    params?: Record<string, unknown>,
    options?: RequestOptions,
  ): Promise<SdkResponse>;
  /** Execute a GET and return response.json(). */
  getJson(url: string, params?: Record<string, unknown>, options?: RequestOptions): Promise<unknown>;
  /** Execute a POST and return response.json(). */
  postJson(
    url: string,
    payload: unknown,
    params?: Record<string, unknown>,
    options?: RequestOptions,
  ): Promise<unknown>;
  /** Read a sensitive asset as bytes. */
  readSensitiveAsset(assetId: number): Promise<Uint8Array>;
  /** Read a sensitive asset as decoded text. */
  readSensitiveText(assetId: number, encoding?: string): Promise<string>;
  /** Publish content or a workspace file as a durable dataset. */
  publishDataset(name: string, options?: PublishDatasetOptions): Promise<DatasetRef>;
  /**
   * Publish a JSON-encoded dataset.
   * @example
   * await this.publishJson('last-item', { id: 'sku-1', ok: true });
   */
  publishJson(name: string, payload: unknown, options?: Omit<PublishDatasetOptions, 'content' | 'contentType'>): Promise<DatasetRef>;
  /** Register a workspace file as a run-local output. */
  registerOutput(handle: string, path: string, options?: RegisterOutputOptions): Promise<LocalOutputHandle>;
  /** Emit one custom metric sample. */
  metric(name: string, value?: number, labels?: Record<string, string>): Promise<void>;
  /** Write text below the run output workspace. */
  writeText(path: string, data: string, encoding?: string): Promise<{ bytes: number }>;
  /** Write bytes below the run output workspace. */
  writeBytes(path: string, data: Uint8Array): Promise<{ bytes: number }>;
}

/** Bind an Agent host to parser instance; platform code owns real hosts. */
export function bindHost(target: object, host: unknown): void;

/** Validate and normalize a custom metric payload before host emission. */
export function metricPayload(name: string, value?: number, labels?: Record<string, string>): {
  name: string;
  value: number;
  labels: Record<string, string>;
};

/** Metadata options for one config field. */
export interface ConfigFieldOptions {
  label?: string | null;
  type?: 'text' | 'number' | 'select' | 'multiselect' | null;
  description?: string | null;
  placeholder?: string | null;
  choices?: unknown[];
  options?: Array<unknown | [unknown, string] | { value: unknown; label?: string }>;
}

/** Parser config metadata extracted into script revision metadata. */
export interface ParserConfig {
  defaults: ConfigObject;
  fields: ConfigObject[];
}

/**
 * Mark one value as parser config metadata.
 * @example
 * start_url: configField('https://example.test', { label: 'Start URL' })
 */
export function configField<T extends ConfigValue>(
  defaultValue: T,
  options?: ConfigFieldOptions,
): T;

/**
 * Build parser config metadata from an object of default values.
 * @example
 * static Config = defineConfig({ retries: configField(2, { type: 'number' }) });
 */
export function defineConfig(shape: Record<string, ConfigValue>): ParserConfig;

/** Common options for parser-declared failures. */
export interface ParserFailureOptions {
  message?: string;
  metadata?: Record<string, unknown>;
}

/** Retry options for the current queue item. */
export interface ItemRetryOptions extends ParserFailureOptions {
  maxAttempts?: number;
  retryDelaySec?: number;
  retry_delay_sec?: number;
}

/** Base class for parser-declared failure intent. */
export class ParserError extends Error {
  reason: string;
  metadata: Record<string, unknown>;
  /** Create a parser-declared failure with a stable reason and optional metadata. */
  constructor(reason: string, options?: ParserFailureOptions);
}

/** Retry the current item with bounded retry metadata. */
export class ItemRetry extends ParserError {
  code: 'item_retry';
  maxAttempts: number;
  retryDelaySec: number | null;
  /**
   * Ask the runtime to retry the current item.
   * @example
   * throw new ItemRetry('rate_limited', { maxAttempts: 3, retryDelaySec: 30 });
   */
  constructor(reason: string, options?: ItemRetryOptions);
}

/** Fail the current item and let the run continue. */
export class ItemFail extends ParserError {
  code: 'item_fail';
  /** Mark the current item failed without failing the whole run. */
  constructor(reason: string, options?: ParserFailureOptions);
}

/** Fail the whole run intentionally. */
export class RunFail extends ParserError {
  code: 'run_fail';
  /** Stop the run with an intentional parser failure. */
  constructor(reason: string, options?: ParserFailureOptions);
}
