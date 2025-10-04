export interface StationData {
  id: string;
  status: "active" | "inactive" | "warning" | "error";
  customer_count: number;
  events: number;
}

export interface EventData {
  timestamp: string;
  event_data: {
    event_name: string;
    station_id: string;
    severity?: "info" | "low" | "medium" | "high" | "critical";
    description?: string;
  };
}

export interface SummaryData {
  total_stations: number;
  active_stations: number;
  total_customers: number;
  total_events: number;
}

export interface EventSummary {
  [eventType: string]: number;
}

export interface SentinelData {
  timestamp: string;
  summary: SummaryData;
  stations: { [stationId: string]: StationData };
  recent_events: EventData[];
  event_summary: EventSummary;
}

export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}
