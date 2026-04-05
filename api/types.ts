export type AnalyticsEvent = {
  eventName: string;
  userId: string;
  timestamp: number;
  properties?: Record<string, any>;
};

export type AnalyticsWorkerConfig = {
  apiKey: string;
  endpoint: string;
  batchSize?: number;
  flushInterval?: number; // in milliseconds
};

export type Batch = {
  events: AnalyticsEvent[];
  retries: number;
};

export type StorageAdapter = {
  storeEvent: (event: AnalyticsEvent) => Promise<void>;
  retrieveEvents: (limit: number) => Promise<AnalyticsEvent[]>;
  removeEvents: (events: AnalyticsEvent[]) => Promise<void>;
  getEventCount: () => Promise<number>;
  clear: () => Promise<void>;
};

export type HttpAdapter = {
  sendEvents: (events: AnalyticsEvent[], apiKey: string, endpoint: string) => Promise<boolean>;
};

export type RetryOptions = {
  maxRetries: number;
  initialDelay: number; // in milliseconds
  backoffFactor: number;
};

export type WorkerState = {
  isRunning: boolean;
  isFlushing: boolean;
};