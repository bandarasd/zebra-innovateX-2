import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from "chart.js";
import { Line, Doughnut } from "react-chartjs-2";
import type { EventSummary, EventData } from "../types/SentinelTypes";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

interface EventsChartProps {
  eventSummary: EventSummary;
  recentEvents: EventData[];
}

export default function EventsChart({
  eventSummary,
  recentEvents,
}: EventsChartProps) {
  // Prepare data for doughnut chart (event distribution)
  const issueEvents = Object.entries(eventSummary)
    .filter(([eventType]) => eventType !== "Success Operation")
    .sort(([, a], [, b]) => b - a);

  const doughnutData = {
    labels: issueEvents.map(([eventType]) => eventType),
    datasets: [
      {
        data: issueEvents.map(([, count]) => count),
        backgroundColor: [
          "#ef4444", // red
          "#f97316", // orange
          "#eab308", // yellow
          "#3b82f6", // blue
          "#8b5cf6", // purple
          "#06b6d4", // cyan
        ],
        borderWidth: 2,
        borderColor: "#ffffff",
      },
    ],
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom" as const,
        labels: {
          padding: 20,
          usePointStyle: true,
        },
      },
      tooltip: {
        callbacks: {
          label: function (context: { label: string; parsed: number }) {
            const total = issueEvents.reduce(
              (sum, [, count]) => sum + count,
              0
            );
            const percentage = ((context.parsed / total) * 100).toFixed(1);
            return `${context.label}: ${context.parsed} (${percentage}%)`;
          },
        },
      },
    },
  };

  // Prepare data for hourly events timeline
  const getHourlyData = () => {
    const hourly = new Array(24).fill(0);
    recentEvents.forEach((event) => {
      const hour = new Date(event.timestamp).getHours();
      hourly[hour]++;
    });
    return hourly;
  };

  const lineData = {
    labels: Array.from(
      { length: 24 },
      (_, i) => `${i.toString().padStart(2, "0")}:00`
    ),
    datasets: [
      {
        label: "Events per Hour",
        data: getHourlyData(),
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: "rgba(0, 0, 0, 0.1)",
        },
      },
      x: {
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Event Distribution */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Event Distribution
        </h3>
        <div className="h-64">
          <Doughnut data={doughnutData} options={doughnutOptions} />
        </div>
      </div>

      {/* Hourly Timeline */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Events Timeline (24h)
        </h3>
        <div className="h-64">
          <Line data={lineData} options={lineOptions} />
        </div>
      </div>
    </div>
  );
}
