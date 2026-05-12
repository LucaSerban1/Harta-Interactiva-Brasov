import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import type { Location } from '../mockData';

interface Props {
  selected: Location | null;
}

export default function MapController({ selected }: Props) {
  const map = useMap();

  useEffect(() => {
    if (selected) {
      map.flyTo([selected.lat, selected.lng], 17, {
        animate: true,
        duration: 1
      });
    }
  }, [selected, map]);

  return null;
}