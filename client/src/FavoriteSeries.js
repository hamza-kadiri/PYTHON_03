import Typography from "@material-ui/core/Typography";
import React from "react";
import Content from "./Slider/Content";

const series = [
  {
    backdrop_path: "/iuiaAx5wNlbDCAO0wiQy0RIlUt.jpg",
    first_air_date: "2015-08-28",
    genre_ids: [80, 18],
    id: 63351,
    name: "Narcos",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Narcos",
    overview:
      "A gritty chronicle of the war against Colombia's infamously violent and powerful drug cartels.",
    popularity: 31.733,
    poster_path: "/rTmal9fDbwh5F0waol2hq35U4ah.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/rTmal9fDbwh5F0waol2hq35U4ah.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/iuiaAx5wNlbDCAO0wiQy0RIlUt.jpg",
    vote_average: 8,
    vote_count: 843
  },
  {
    backdrop_path: "/m7GsWHPl6O9hEXZ7eKDCUFTafCD.jpg",
    first_air_date: "2018-11-16",
    genre_ids: [80, 18],
    id: 80968,
    name: "Narcos: Mexico",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Narcos: Mexico",
    overview:
      "See the rise of the Guadalajara Cartel as an American DEA agent learns the danger of targeting narcos in 1980s Mexico.",
    popularity: 12.532,
    poster_path: "/aXwMx8OvRFMfI1RmkbJm6Bq1jVg.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/aXwMx8OvRFMfI1RmkbJm6Bq1jVg.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/m7GsWHPl6O9hEXZ7eKDCUFTafCD.jpg",
    vote_average: 8.1,
    vote_count: 53
  },
  {
    backdrop_path: "/xIvlXYY65vQtPIONWNGdFQWlzoV.jpg",
    first_air_date: "2018-08-02",
    genre_ids: [99],
    id: 84956,
    name: "Meet the Drug Lords: Inside the Real Narcos",
    origin_country: [],
    original_language: "en",
    original_name: "Meet the Drug Lords: Inside the Real Narcos",
    overview:
      "Ex-Special Forces soldier Jason Fox used to hunt drug lords for a living. Now, he heads unarmed into the heart of Latin America's billion-dollar cartels.",
    popularity: 0.72,
    poster_path: "/1kkzGRqjZndgao4WdzNu5bK0CwS.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/1kkzGRqjZndgao4WdzNu5bK0CwS.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/xIvlXYY65vQtPIONWNGdFQWlzoV.jpg",
    vote_average: 7.7,
    vote_count: 3
  },
  {
    backdrop_path: "/uRhTOc2zVL95z3lJDVVSoUhVmar.jpg",
    first_air_date: "2019-07-30",
    genre_ids: [],
    id: 91751,
    name: "60 Days In: Narcoland",
    origin_country: ["US"],
    original_language: "en",
    original_name: "60 Days In: Narcoland",
    overview:
      "Six participants go undercover in crucial areas along I-65 – one of the biggest drug trafficking corridors in the country, encompassing six counties in Kentucky and Indiana – for a first-hand look into how drug cartels have infiltrated America’s Heartland.",
    popularity: 1.358,
    poster_path: "/gqSpbCNmv58KF1fUYscdZkQbSL0.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/gqSpbCNmv58KF1fUYscdZkQbSL0.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/uRhTOc2zVL95z3lJDVVSoUhVmar.jpg",
    vote_average: 10,
    vote_count: 1
  },
  {
    backdrop_path: null,
    first_air_date: "2018-07-18",
    genre_ids: [99],
    id: 89831,
    name: "Die echten Narcos",
    origin_country: [],
    original_language: "de",
    original_name: "Die echten Narcos",
    overview: "",
    popularity: 0.6,
    poster_path: "/h1gx74KvC4CxYDu0nGFBIa9ScL1.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/h1gx74KvC4CxYDu0nGFBIa9ScL1.jpg",
    vote_average: 0,
    vote_count: 0
  }
];

const FavoriteSeries = ({ match }) => (
  <React.Fragment>
    <div
      style={{
        alignItems: "flex-start",
        paddingTop: "4rem",
        height: "calc(100vh - 4rem)",
        width: "100%"
      }}
    >
      <React.Fragment>
        <Typography style={{ marginLeft: "10px" }} variant="h4" component="h4">
          Your Favorite Series
        </Typography>
        {series.map(serie => (
          <Content serie={serie}></Content>
        ))}
      </React.Fragment>
    </div>
  </React.Fragment>
);

export default FavoriteSeries;
