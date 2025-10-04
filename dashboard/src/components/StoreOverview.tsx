import type { SummaryData } from "../types/SentinelTypes";

interface StoreOverviewProps {
  summary: SummaryData;
}

export default function StoreOverview({ summary }: StoreOverviewProps) {
  const metrics = [
    {
      title: "Total Stations",
      value: summary.total_stations,
      icon: "🏪",
      color: "bg-blue-500",
      trend: "+5%",
    },
    {
      title: "Active Stations",
      value: summary.active_stations,
      icon: "✅",
      color: "bg-green-500",
      trend: "+2%",
    },
    {
      title: "Total Customers",
      value: summary.total_customers,
      icon: "👥",
      color: "bg-purple-500",
      trend: "+12%",
    },
    {
      title: "Total Events",
      value: summary.total_events,
      icon: "⚠️",
      color: "bg-orange-500",
      trend: "-8%",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric, index) => (
        <div
          key={metric.title}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-slideIn"
          style={{ animationDelay: `${index * 100}ms` }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">
                {metric.title}
              </p>
              <p className="text-3xl font-bold text-gray-900">{metric.value}</p>
              <div className="flex items-center mt-2">
                <span
                  className={`text-xs font-medium px-2 py-1 rounded-full ${
                    metric.trend.startsWith("+")
                      ? "bg-green-100 text-green-800"
                      : "bg-red-100 text-red-800"
                  }`}
                >
                  {metric.trend}
                </span>
                <span className="text-xs text-gray-500 ml-2">vs last week</span>
              </div>
            </div>
            <div
              className={`w-12 h-12 rounded-lg ${metric.color} flex items-center justify-center text-white text-xl`}
            >
              {metric.icon}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
