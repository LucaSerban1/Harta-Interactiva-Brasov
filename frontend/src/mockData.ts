export interface Location {
  id: number;
  name: string;
  lat: number;
  lng: number;
  category: string;
  description?: string;
  rating_avg?: number;
  rating?: number;
  address?: string;
  tags?: string[];
  is_verified?: boolean;
  photos?: string[];
  reviews?: Review[];
}

export interface Review {
  id: number;
  user: string;
  text: string;
  rating: number;
  date: string;
}

export const mockLocations: Location[] = [
  {
    id: 1,
    name: "Cafeneaua Sergiana",
    address: "Str. Mureșenilor 28, Brașov",
    category: "cafe",
    rating: 4.5,
    lat: 45.6427,
    lng: 25.5887,
    photos: [
      "https://placehold.co/400x250?text=Sergiana+1",
      "https://placehold.co/400x250?text=Sergiana+2",
    ],
    reviews: [
      { id: 1, user: "Andrei", text: "Cafea excelentă, atmosferă liniștită", rating: 5, date: "2026-04-10" },
      { id: 2, user: "Maria", text: "Bun pentru lucrat, wifi stabil", rating: 4, date: "2026-04-08" },
    ],
  },
  {
    id: 2,
    name: "Biblioteca Județeană",
    address: "Bd. Eroilor 35, Brașov",
    category: "library",
    rating: 4.2,
    lat: 45.6440,
    lng: 25.5910,
    photos: [
      "https://placehold.co/400x250?text=Biblioteca+1",
      "https://placehold.co/400x250?text=Biblioteca+2",
    ],
    reviews: [
      { id: 3, user: "Ion", text: "Liniște totală, recomandat pentru studiu", rating: 5, date: "2026-04-15" },
      { id: 4, user: "Elena", text: "Multe resurse disponibile", rating: 4, date: "2026-04-12" },
    ],
  },
  {
    id: 3,
    name: "Parc Titulescu",
    address: "Str. Nicolae Titulescu, Brașov",
    category: "park",
    rating: 4.0,
    lat: 45.6380,
    lng: 25.5950,
    photos: [
      "https://placehold.co/400x250?text=Parc+1",
    ],
    reviews: [
      { id: 5, user: "Radu", text: "Perfect pentru pauze între cursuri", rating: 4, date: "2026-04-20" },
    ],
  },
  {
    id: 4,
    name: "Cowork Brașov",
    address: "Str. Lungă 10, Brașov",
    category: "cowork",
    rating: 4.7,
    lat: 45.6455,
    lng: 25.5875,
    photos: [
      "https://placehold.co/400x250?text=Cowork+1",
      "https://placehold.co/400x250?text=Cowork+2",
    ],
    reviews: [
      { id: 6, user: "Daria", text: "Spațiu modern, prize la fiecare loc", rating: 5, date: "2026-04-18" },
      { id: 7, user: "Mihai", text: "Puțin scump dar merită", rating: 4, date: "2026-04-16" },
    ],
  },
];