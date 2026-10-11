import { useEffect, useState } from 'react';
import { getEvents } from '../api/client';

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadEvents = async () => {
    try {
      const data = await getEvents(100);
      setEvents(data.events || []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
    const interval = setInterval(loadEvents, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="p-8 text-slate-400">Loading...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-2">Live Events</h1>
      <p className="text-slate-400 mb-8">All canary triggers (updates every 5 sec)</p>

      {events.length === 0 ? (
        <p className="text-slate-500">No events yet.</p>
      ) : (
        <div className="space-y-3">
          {events.map((event) => (
            <div key={event.id} className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <span className="font-mono text-emerald-400">{event.token_id}</span>
                <span className="px-2 py-1 rounded text-xs font-bold bg-slate-700 text-slate-300">
                  {event.threat_level}
                </span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm text-slate-400">
                <div>IP: <span className="font-mono">{event.source_ip}</span></div>
                <div>Event: {event.event_name}</div>
                <div>Country: {event.geo?.country || 'N/A'}</div>
                <div>Abuse: {event.abuse_score || 0}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
