import "../App.css";
import { DateTime } from "luxon";
import { useEffect, useState } from "react";

function Clock() {
  const [date, setDate] = useState(DateTime.now());

  useEffect(() => {
    const interval = setInterval(() => {
      setDate(DateTime.now());
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <div className="date">{date.toLocaleString(DateTime.DATE_MED)}</div>;
}

export default Clock;
