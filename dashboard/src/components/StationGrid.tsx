import type { StationData } from "../types/SentinelTypes";

interface StationGridProps {
  stations: { [stationId: string]: StationData };
}

export default function StationGrid({ stations }: StationGridProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-500";
      case "warning":
        return "bg-yellow-500";
      case "error":
        return "bg-red-500";
      case "inactive":
        return "bg-gray-400";
      default:
        return "bg-gray-400";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "active":
        return "Active";
      case "warning":
        return "Warning";
      case "error":
        return "Error";
      case "inactive":
        return "Inactive";
      default:
        return "Unknown";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return "✅";
      case "warning":
        return "⚠️";
      case "error":
        return "❌";
      case "inactive":
        return "⭕";
      default:
        return "❓";
    }
  };

  const stationList = Object.values(stations).sort((a, b) =>
    a.id.localeCompare(b.id)
  );

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Station Status</h3>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-sm text-gray-600">
              {stationList.filter((s) => s.status === "active").length} Active
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-sm text-gray-600">
              {stationList.filter((s) => s.status === "error").length} Error
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
        {stationList.map((station) => (
          <div
            key={station.id}
            className={`relative p-4 rounded-lg border-2 transition-all duration-200 hover:shadow-md ${
              station.status === "active"
                ? "border-green-200 bg-green-50"
                : station.status === "warning"
                ? "border-yellow-200 bg-yellow-50"
                : station.status === "error"
                ? "border-red-200 bg-red-50"
                : "border-gray-200 bg-gray-50"
            }`}
          >
            {/* Status indicator */}
            <div className="absolute top-2 right-2">
              <div
                className={`w-3 h-3 rounded-full ${getStatusColor(
                  station.status
                )} animate-pulse-slow`}
              ></div>
            </div>

            {/* Station info */}
            <div className="text-center">
              <div className="text-2xl mb-2">
                {getStatusIcon(station.status)}
              </div>
              <div className="font-semibold text-gray-900 mb-1">
                {station.id}
              </div>
              <div
                className={`text-xs font-medium mb-3 ${
                  station.status === "active"
                    ? "text-green-700"
                    : station.status === "warning"
                    ? "text-yellow-700"
                    : station.status === "error"
                    ? "text-red-700"
                    : "text-gray-500"
                }`}
              >
                {getStatusText(station.status)}
              </div>

              {/* Metrics */}
              <div className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-gray-500">Customers:</span>
                  <span className="font-medium text-gray-900">
                    {station.customer_count}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-gray-500">Events:</span>
                  <span
                    className={`font-medium ${
                      station.events > 0 ? "text-red-600" : "text-green-600"
                    }`}
                  >
                    {station.events}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
