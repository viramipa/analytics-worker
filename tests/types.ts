export type EventType =
  | 'page_view'
  | 'button_click'
  | 'form_submission'
  | 'video_play'
  | 'video_pause'
  | 'custom';

export interface UserContext {
  userId?: string;
  sessionId?: string;
  deviceId?: string;
  ipAddress?: string;
  userAgent?: string;
}

export interface EventProperties {
  [key: string]: string | number | boolean | null | undefined | EventProperties | (string | number | boolean | null | undefined | EventProperties)[];
}

export interface AnalyticsEvent {
  eventType: EventType;
  timestamp: number;
  userContext: UserContext;
  properties?: EventProperties;
}

export interface AnalyticsWorkerConfig {
  apiKey: string;
  endpoint: string;
  batchSize?: number;
  flushInterval?: number; // in milliseconds
  debug?: boolean;
}

export interface QueueMessage {
  event: AnalyticsEvent;
}

export interface ApiResponse {
  success: boolean;
  message?: string;
  statusCode: number;
}