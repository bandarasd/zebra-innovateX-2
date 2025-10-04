import { useState, useEffect } from "react";
import Dashboard from "./components/Dashboard";
import type { SentinelData, StationData } from "./types/SentinelTypes";

const API_BASE_URL = "http://localhost:8081";

function App() {
  const [data, setData] = useState<SentinelData | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/data`);
        if (response.ok) {
          const backendData = await response.json();

          // Transform backend data to match frontend types
          const transformedData: SentinelData = {
            timestamp: backendData.timestamp,
            summary: backendData.summary,
            stations: transformStations(backendData.stations || {}),
            recent_events: backendData.recent_events || [],
            event_summary: backendData.event_summary || {},
          };

          setData(transformedData);
          setIsConnected(true);
          setLastUpdate(new Date());
        } else {
          setIsConnected(false);
          setMockData();
        }
      } catch (error) {
        console.error("Failed to fetch data:", error);
        setIsConnected(false);
        setMockData();
      } finally {
        setLoading(false);
      }
    };

    // Transform backend station format to frontend format
    const transformStations = (backendStations: Record<string, unknown>) => {
      const transformed: { [stationId: string]: StationData } = {};

      Object.entries(backendStations).forEach(
        ([stationId, stationData]: [string, unknown]) => {
          const station = stationData as Record<string, unknown>;
          transformed[stationId] = {
            id: stationId,
            status:
              ((station.status as string)?.toLowerCase() as
                | "active"
                | "inactive"
                | "warning"
                | "error") || "inactive",
            customer_count: (station.customer_count as number) || 0,
            events: 0, // Will be calculated from recent_events if needed
          };
        }
      );

      return transformed;
    };

    const setMockData = () => {
      const mockData: SentinelData = {
        timestamp: new Date().toISOString(),
        summary: {
          total_stations: 12,
          active_stations: 9,
          total_customers: 67,
          total_events: 23,
        },
        stations: {
          SCC1: { id: "SCC1", status: "active", customer_count: 3, events: 2 },
          SCC2: { id: "SCC2", status: "active", customer_count: 1, events: 0 },
          SCC3: { id: "SCC3", status: "warning", customer_count: 0, events: 1 },
          SCC4: { id: "SCC4", status: "active", customer_count: 2, events: 3 },
          SCC5: {
            id: "SCC5",
            status: "inactive",
            customer_count: 0,
            events: 0,
          },
          SCC6: { id: "SCC6", status: "active", customer_count: 4, events: 1 },
          SCC7: { id: "SCC7", status: "active", customer_count: 2, events: 0 },
          SCC8: { id: "SCC8", status: "error", customer_count: 0, events: 5 },
          SCC9: { id: "SCC9", status: "active", customer_count: 1, events: 1 },
          SCC10: {
            id: "SCC10",
            status: "active",
            customer_count: 3,
            events: 0,
          },
          SCC11: {
            id: "SCC11",
            status: "inactive",
            customer_count: 0,
            events: 0,
          },
          SCC12: {
            id: "SCC12",
            status: "active",
            customer_count: 2,
            events: 2,
          },
        },
        recent_events: [
          {
            timestamp: "2025-10-04T00:30:15",
            event_data: {
              event_name: "Scanner Avoidance",
              station_id: "SCC1",
              severity: "high",
            },
          },
          {
            timestamp: "2025-10-04T00:29:42",
            event_data: {
              event_name: "Barcode Switching",
              station_id: "SCC4",
              severity: "high",
            },
          },
          {
            timestamp: "2025-10-04T00:29:18",
            event_data: {
              event_name: "Weight Discrepancy",
              station_id: "SCC8",
              severity: "medium",
            },
          },
          {
            timestamp: "2025-10-04T00:28:55",
            event_data: {
              event_name: "Long Queue Length",
              station_id: "SCC6",
              severity: "low",
            },
          },
          {
            timestamp: "2025-10-04T00:28:33",
            event_data: {
              event_name: "Success Operation",
              station_id: "SCC2",
              severity: "info",
            },
          },
          {
            timestamp: "2025-10-04T00:28:10",
            event_data: {
              event_name: "System Crash",
              station_id: "SCC8",
              severity: "critical",
            },
          },
        ],
        event_summary: {
          "Scanner Avoidance": 8,
          "Barcode Switching": 5,
          "Weight Discrepancy": 3,
          "Long Queue Length": 4,
          "System Crash": 2,
          "Success Operation": 45,
        },
      };
      setData(mockData);
      setLastUpdate(new Date());
    };

    // Initial fetch
    fetchData();

    // Set up polling every 3 seconds
    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            🛒 Project Sentinel
          </h1>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">
                🛒 Project Sentinel
              </h1>
              <span className="ml-3 px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                Retail Analytics
              </span>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    isConnected
                      ? "bg-green-500 animate-pulse-slow"
                      : "bg-red-500"
                  }`}
                ></div>
                <span
                  className={`text-sm font-medium ${
                    isConnected ? "text-green-700" : "text-red-700"
                  }`}
                >
                  {isConnected ? "Connected" : "Mock Data"}
                </span>
              </div>

              {lastUpdate && (
                <span className="text-sm text-gray-500">
                  Last update: {lastUpdate.toLocaleTimeString()}
                </span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {data ? (
          <Dashboard data={data} />
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 text-lg">No data available</div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
