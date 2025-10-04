import type { EventSummary as EventSummaryType } from "../types/SentinelTypes";

interface EventSummaryProps {
  eventSummary: EventSummaryType;
}

export default function EventSummary({ eventSummary }: EventSummaryProps) {
  const getEventColor = (eventType: string) => {
    const colors: { [key: string]: string } = {
      "Scanner Avoidance": "bg-red-500",
      "Barcode Switching": "bg-orange-500",
      "Weight Discrepancy": "bg-yellow-500",
      "Long Queue Length": "bg-blue-500",
      "System Crash": "bg-purple-500",
      "Success Operation": "bg-green-500",
    };
    return colors[eventType] || "bg-gray-500";
  };

  const getEventIcon = (eventType: string) => {
    const icons: { [key: string]: string } = {
      "Scanner Avoidance": "🚫",
      "Barcode Switching": "🔄",
      "Weight Discrepancy": "⚖️",
      "Long Queue Length": "⏰",
      "System Crash": "💥",
      "Success Operation": "✅",
    };
    return icons[eventType] || "📊";
  };

  const getSeverityLevel = (eventType: string, count: number) => {
    if (eventType === "Success Operation") return "success";
    if (count >= 8) return "critical";
    if (count >= 5) return "high";
    if (count >= 3) return "medium";
    return "low";
  };

  const sortedEvents = Object.entries(eventSummary)
    .sort(([, a], [, b]) => b - a)
    .filter(([eventType]) => eventType !== "Success Operation");

  const successOperations = eventSummary["Success Operation"] || 0;
  const totalIssues = sortedEvents.reduce((sum, [, count]) => sum + count, 0);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Event Summary</h3>
        <div className="flex items-center space-x-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {successOperations}
            </div>
            <div className="text-xs text-gray-500">Success</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">{totalIssues}</div>
            <div className="text-xs text-gray-500">Issues</div>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {sortedEvents.map(([eventType, count]) => {
          const severity = getSeverityLevel(eventType, count);
          return (
            <div
              key={eventType}
              className="flex items-center justify-between p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div
                  className={`w-10 h-10 rounded-lg ${getEventColor(
                    eventType
                  )} flex items-center justify-center text-white`}
                >
                  {getEventIcon(eventType)}
                </div>
                <div>
                  <div className="font-medium text-gray-900">{eventType}</div>
                  <div
                    className={`text-xs font-medium capitalize ${
                      severity === "critical"
                        ? "text-red-600"
                        : severity === "high"
                        ? "text-orange-600"
                        : severity === "medium"
                        ? "text-yellow-600"
                        : "text-green-600"
                    }`}
                  >
                    {severity} severity
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-900">{count}</div>
                <div className="text-xs text-gray-500">events</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
