import type { SentinelData } from "../types/SentinelTypes";
import StoreOverview from "./StoreOverview";
import EventSummary from "./EventSummary";
import StationGrid from "./StationGrid";
import RecentEvents from "./RecentEvents";
import EventsChart from "./EventsChart";

interface DashboardProps {
  data: SentinelData;
}

export default function Dashboard({ data }: DashboardProps) {
  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <StoreOverview summary={data.summary} />

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Event Summary - Full width on mobile, spans 2 columns on large screens */}
        <div className="lg:col-span-2 space-y-6">
          <EventSummary eventSummary={data.event_summary} />
          <EventsChart
            eventSummary={data.event_summary}
            recentEvents={data.recent_events}
          />
        </div>

        {/* Recent Events - Sidebar */}
        <div className="lg:col-span-1">
          <RecentEvents events={data.recent_events} />
        </div>
      </div>

      {/* Station Grid - Full width */}
      <StationGrid stations={data.stations} />
    </div>
  );
}
