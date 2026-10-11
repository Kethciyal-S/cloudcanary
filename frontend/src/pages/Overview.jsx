import { useEffect, useState } from 'react';
import { getStats, getEvents } from '../api/client';

export default function Overview() {
  const [stats, setStats] = useState(null);
  const [recentEvents, setRecentEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [statsData, eventsData] = await Promise.all([
        getStats(),
        getEvents(5),
      ]);
      setStats(statsData);
      setRecentEvents(eventsData.events || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="p-8 text-slate-400">Loading...</div>;

  const cards = [
    { label: 'Total Triggers', value: stats?.total_triggers || 0, color: 'text-blue-400' },
    { label: 'Critical Threats', value: stats?.critical_threats || 0, color: 'text-red-400' },
    { label: 'High Threats', value: stats?.high_threats || 0, color: 'text-orange-400' },
    { label: 'Unique Attackers', value: stats?.unique_attackers || 0, color: 'text-purple-400' },
  ];

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-2">Dashboard Overview</h1>
      <p className="text-slate-400 mb-8">Real-time canary trigger monitoring</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {cards.map((card) => (
          <div key={card.label} className="bg-slate-900 border border-slate-800 rounded-lg p-6">
            <p className="text-slate-400 text-sm mb-2">{card.label}</p>
            <p className={`text-4xl font-bold ${card.color}`}>{card.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Recent Canary Triggers</h2>
        {recentEvents.length === 0 ? (
          <p className="text-slate-500">No events yet. Plant a canary token to start.</p>
        ) : (
          <div className="space-y-3">
            {recentEvents.map((event) => (
              <div key={event.id} className="flex justify-between items-center p-3 bg-slate-800 rounded">
                <div>
                  <p className="font-mono text-sm text-emerald-400">{event.token_id}</p>
                  <p className="text-xs text-slate-400">{event.source_ip} · {event.event_name}</p>
                </div>
                <span className={`px-3 py-1 rounded text-xs font-bold ${
                  event.threat_level === 'critical' ? 'bg-red-500/20 text-red-400' :
                  'bg-slate-700 text-slate-300'
                }`}>
                  {event.threat_level}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
