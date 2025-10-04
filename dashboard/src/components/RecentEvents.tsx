import type { EventData } from "../types/SentinelTypes";

interface RecentEventsProps {
  events: EventData[];
}

export default function RecentEvents({ events }: RecentEventsProps) {
  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case "critical":
        return "bg-red-600 text-white";
      case "high":
        return "bg-red-500 text-white";
      case "medium":
        return "bg-yellow-500 text-white";
      case "low":
        return "bg-blue-500 text-white";
      case "info":
        return "bg-green-500 text-white";
      default:
        return "bg-gray-500 text-white";
    }
  };

  const getEventIcon = (eventName: string) => {
    const icons: { [key: string]: string } = {
      "Scanner Avoidance": "🚫",
      "Barcode Switching": "🔄",
      "Weight Discrepancy": "⚖️",
      "Long Queue Length": "⏰",
      "System Crash": "💥",
      "Success Operation": "✅",
    };
    return icons[eventName] || "📊";
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const getTimeAgo = (timestamp: string) => {
    const now = new Date();
    const eventTime = new Date(timestamp);
    const diffMs = now.getTime() - eventTime.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${Math.floor(diffHours / 24)}d ago`;
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 h-fit">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Recent Events</h3>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-500">Live</span>
        </div>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
        {events.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">📋</div>
            <div>No recent events</div>
          </div>
        ) : (
          events.map((event, index) => (
            <div
              key={`${event.timestamp}-${index}`}
              className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors animate-slideIn"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm">
                  {getEventIcon(event.event_data.event_name)}
                </div>
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {event.event_data.event_name}
                  </p>
                  {event.event_data.severity && (
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(
                        event.event_data.severity
                      )}`}
                    >
                      {event.event_data.severity}
                    </span>
                  )}
                </div>

                <div className="flex items-center justify-between">
                  <p className="text-sm text-gray-500">
                    Station {event.event_data.station_id}
                  </p>
                  <div className="text-right">
                    <p className="text-xs text-gray-400">
                      {formatTime(event.timestamp)}
                    </p>
                    <p className="text-xs text-gray-400">
                      {getTimeAgo(event.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {events.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <button className="w-full text-sm text-blue-600 hover:text-blue-800 font-medium">
            View all events →
          </button>
        </div>
      )}
    </div>
  );
}
