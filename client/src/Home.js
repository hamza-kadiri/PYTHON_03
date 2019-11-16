import { Typography } from "@material-ui/core";
import React from "react";
import { connect } from "react-redux";
import Slider from "./Slider";

const mockedSuggestions = [
  {
    backdrop_path: "/27cshLy9anL9G0g6tBQjWkPACx5.jpg",
    first_air_date: "2003-09-21",
    genre_ids: [35],
    id: 2691,
    name: "Two and a Half Men",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Two and a Half Men",
    overview:
      "A hedonistic jingle writer's free-wheeling life comes to an abrupt halt when his brother and 10-year-old nephew move into his beach-front house.",
    popularity: 84.836,
    poster_path: "/A9QDK4OWpv41W27kCv0LXe30k9S.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/A9QDK4OWpv41W27kCv0LXe30k9S.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/27cshLy9anL9G0g6tBQjWkPACx5.jpg",
    vote_average: 6.4,
    vote_count: 770
  },
  {
    backdrop_path: "/s8OiqMrNrnDMTwczcuHdyM0Qc7r.jpg",
    first_air_date: "1983-01-23",
    genre_ids: [10759],
    id: 1516,
    name: "The A-Team",
    origin_country: ["US"],
    original_language: "en",
    original_name: "The A-Team",
    overview:
      'The A-Team is an American action-adventure television series, running from 1983 to 1987, about a fictional group of ex United States Army Special Forces personnel who work as soldiers of fortune, while on the run from the Army after being branded as war criminals for a "crime they didn\'t commit".',
    popularity: 35.808,
    poster_path: "/g0BmuMvzzlqO75iri3vkUNLM4LI.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/g0BmuMvzzlqO75iri3vkUNLM4LI.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/s8OiqMrNrnDMTwczcuHdyM0Qc7r.jpg",
    vote_average: 7.1,
    vote_count: 230
  },
  {
    backdrop_path: "/2TEtOFNhGsvHK21U7lmFDD5rZC0.jpg",
    first_air_date: "2011-10-23",
    genre_ids: [18, 10765],
    id: 39272,
    name: "Once Upon a Time",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Once Upon a Time",
    overview:
      "There is a town in Maine where every story book character you've ever known is trapped between two worlds, victims of a powerful curse. Only one knows the truth and only one can break the spell.\n\nEmma Swan is a 28-year-old bail bonds collector who has been supporting herself since she was abandoned as a baby. Things change for her when her son Henry, whom she abandoned years ago, finds her and asks for her help explaining that she is from a different world where she is Snow White's missing daughter.",
    popularity: 36.737,
    poster_path: "/49qD372jeHUTmdNMGJkjCFZdv9y.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/49qD372jeHUTmdNMGJkjCFZdv9y.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/2TEtOFNhGsvHK21U7lmFDD5rZC0.jpg",
    vote_average: 6.5,
    vote_count: 874
  },
  {
    backdrop_path: "/2Qx3fM9x0QW3i0BzqdjbUK2jPc5.jpg",
    first_air_date: "2002-09-26",
    genre_ids: [18, 9648, 10759],
    id: 2593,
    name: "Without a Trace",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Without a Trace",
    overview:
      "The series follows the ventures of a Missing Persons Unit of the FBI in New York City.",
    popularity: 25.614,
    poster_path: "/2VvFNKBZqGe8sxA7hgyIN8ta8mN.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/2VvFNKBZqGe8sxA7hgyIN8ta8mN.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/2Qx3fM9x0QW3i0BzqdjbUK2jPc5.jpg",
    vote_average: 6.8,
    vote_count: 86
  },
  {
    backdrop_path: "/g0VmdXoH88kHxqXLIgg46sQLPzt.jpg",
    first_air_date: "2015-04-20",
    genre_ids: [18],
    id: 62455,
    name: "Locked Up",
    origin_country: ["ES"],
    original_language: "es",
    original_name: "Vis a vis",
    overview:
      "Set up to take the blame for corporate fraud, young Macarena Ferreiro is locked up in a high-security women's prison surrounded by tough, ruthless criminals in this tense, provocative Spanish thriller.",
    popularity: 27.363,
    poster_path: "/gy1lzy6pPOE49Wbgenw1SlKGsZa.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/gy1lzy6pPOE49Wbgenw1SlKGsZa.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/g0VmdXoH88kHxqXLIgg46sQLPzt.jpg",
    vote_average: 7.3,
    vote_count: 50
  },
  {
    backdrop_path: "/4HL9fbOORVFmR4D3shsRtIDZyNs.jpg",
    first_air_date: "2008-05-22",
    genre_ids: [10763, 10767],
    id: 7562,
    name: "Q&A",
    origin_country: ["AU"],
    original_language: "en",
    original_name: "Q&A",
    overview:
      "Hosted by Tony Jones, Q&amp;A puts punters, pollies and pundits together in the studio to thrash out the hot issues of the week. It's about democracy in action - the audience gets to ask the questions.",
    popularity: 22.051,
    poster_path: "/1GIkSqvtOLtQlg3PfEvEW6xJDuL.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/1GIkSqvtOLtQlg3PfEvEW6xJDuL.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/4HL9fbOORVFmR4D3shsRtIDZyNs.jpg",
    vote_average: 4.5,
    vote_count: 2
  },
  {
    backdrop_path: "/yE2IH4ZPz9Yl2f0eYp2tzc8JXA.jpg",
    first_air_date: "1972-09-17",
    genre_ids: [35, 18, 10768],
    id: 918,
    name: "M*A*S*H",
    origin_country: ["US"],
    original_language: "en",
    original_name: "M*A*S*H",
    overview:
      "The 4077th Mobile Army Surgical Hospital is stuck in the middle of the Korean war. With little help from the circumstances they find themselves in, they are forced to make their own fun. Fond of practical jokes and revenge, the doctors, nurses, administrators, and soldiers often find ways of making wartime life bearable.",
    popularity: 25.808,
    poster_path: "/cvLmJp8AhaddlDxoYrU3TN8uXPm.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/cvLmJp8AhaddlDxoYrU3TN8uXPm.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/yE2IH4ZPz9Yl2f0eYp2tzc8JXA.jpg",
    vote_average: 7.8,
    vote_count: 281
  },
  {
    backdrop_path: "/olkaZfDqfDSbRCUcAEK4mmqko5g.jpg",
    first_air_date: "2018-09-26",
    genre_ids: [18],
    id: 81499,
    name: "A Million Little Things",
    origin_country: ["US"],
    original_language: "en",
    original_name: "A Million Little Things",
    overview:
      "A group of friends from Boston who feel stuck in life experience an unexpected wake-up call after one of their friend dies unexpectedly.",
    popularity: 33.331,
    poster_path: "/ecE1yxIYUYHumtXBJ2PQvuCm7En.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/ecE1yxIYUYHumtXBJ2PQvuCm7En.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/olkaZfDqfDSbRCUcAEK4mmqko5g.jpg",
    vote_average: 6.8,
    vote_count: 19
  },
  {
    backdrop_path: "/AuY5Wuiwgc2CeuzM0I2poSe4E0x.jpg",
    first_air_date: "2017-11-02",
    genre_ids: [80, 18, 10759],
    id: 71790,
    name: "S.W.A.T.",
    origin_country: ["US"],
    original_language: "en",
    original_name: "S.W.A.T.",
    overview:
      "Follows a locally born and bred S.W.A.T. lieutenant who is torn between loyalty to the streets and duty to his fellow officers when he's tasked to run a highly-trained unit that's the last stop for solving crimes in Los Angeles.",
    popularity: 52.077,
    poster_path: "/dM1WYFrRtnkOZR1oVtCpBhscoPu.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/dM1WYFrRtnkOZR1oVtCpBhscoPu.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/AuY5Wuiwgc2CeuzM0I2poSe4E0x.jpg",
    vote_average: 7.1,
    vote_count: 161
  },
  {
    backdrop_path: "/hK5YFwhQNMrB3EFeAJsVYh9rmS0.jpg",
    first_air_date: "2005-10-28",
    genre_ids: [99],
    id: 4038,
    name: "A Haunting",
    origin_country: ["US"],
    original_language: "en",
    original_name: "A Haunting",
    overview:
      "These are the true stories of the innocent and the unimaginable. Based on true events, A Haunting dramatises some of the scariest stories, revealing a world in which tragedy, suicide and murder have left psychic impressions so powerful that innocent people become forced to deal with them decades later. Through mesmerising first-person accounts, the mystery and origin of each haunting is powerfully revealed and leaves a lingering sense that life - and death - are much stronger then anyone could have possibly imagined.",
    popularity: 11.351,
    poster_path: "/kFZE6lPpqQhf9unGynmosOiRxUI.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/kFZE6lPpqQhf9unGynmosOiRxUI.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/hK5YFwhQNMrB3EFeAJsVYh9rmS0.jpg",
    vote_average: 6.1,
    vote_count: 28
  },
  {
    backdrop_path: "/dfEmmE3RJh3OYxyqOFDBt0qMS0E.jpg",
    first_air_date: "2013-10-06",
    genre_ids: [16],
    id: 60761,
    name: "Ace of Diamond",
    origin_country: ["JP"],
    original_language: "ja",
    original_name: "ダイヤのA",
    overview:
      "Eijun Sawamura is a pitcher who joins an elite school with a brilliant catcher named Kazuya Miyuki. Together with the rest of the team, they strive for Japan's storied Koushien championships through hard work and determination.",
    popularity: 20.033,
    poster_path: "/af6UFbW6VvVwfsM4vtGD9k5o03J.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/af6UFbW6VvVwfsM4vtGD9k5o03J.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/dfEmmE3RJh3OYxyqOFDBt0qMS0E.jpg",
    vote_average: 6.4,
    vote_count: 5
  },
  {
    backdrop_path: "/fftR6mAKZMNKhmuHyG4YkyTyl1U.jpg",
    first_air_date: "2018-09-14",
    genre_ids: [18, 10765],
    id: 77236,
    name: "A Discovery of Witches",
    origin_country: ["GB"],
    original_language: "en",
    original_name: "A Discovery of Witches",
    overview:
      "Diana Bishop, historian and witch, accesses Ashmole 782 and knows she must solve its mysteries. She is offered help by the enigmatic Matthew Clairmont, but he's a vampire and witches should never trust vampires.",
    popularity: 19.517,
    poster_path: "/tSUoJXxI45KUhqe1qiD2gNtJgzd.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/tSUoJXxI45KUhqe1qiD2gNtJgzd.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/fftR6mAKZMNKhmuHyG4YkyTyl1U.jpg",
    vote_average: 7.8,
    vote_count: 86
  },
  {
    backdrop_path: "/9XgVqYPY7gDuCpymmTwwpXA1IB5.jpg",
    first_air_date: "2017-01-13",
    genre_ids: [35, 18, 9648, 10751],
    id: 65294,
    name: "A Series of Unfortunate Events",
    origin_country: ["US"],
    original_language: "en",
    original_name: "A Series of Unfortunate Events",
    overview:
      "The orphaned Baudelaire children face trials, tribulations and the evil Count Olaf, all in their quest to uncover the secret of their parents' death.",
    popularity: 27.755,
    poster_path: "/chLSPHjb1dAZRKstpx17lnDbZU9.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/chLSPHjb1dAZRKstpx17lnDbZU9.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/9XgVqYPY7gDuCpymmTwwpXA1IB5.jpg",
    vote_average: 6.9,
    vote_count: 265
  },
  {
    backdrop_path: null,
    first_air_date: "1981-11-18",
    genre_ids: [10766, 18],
    id: 4328,
    name: "A Country Practice",
    origin_country: ["AU"],
    original_language: "en",
    original_name: "A Country Practice",
    overview:
      "A Country Practice was an Australian television drama series. At its inception, one of the longest-running of its kind, produced by James Davern of JNP Productions, who had wrote the pilot episode and entered a script contest for the network in 1979, coming third and winning a merit award. It ran on the Seven Network for 1,058 episodes from 18 November 1981 to 22 November 1993. It was produced in ATN-7's production facility at Epping, Sydney. After its lengthy run on the seven network it was picked up by network ten with a mainly new cast from April to November 1994 for 30 episodes, although the ten series was not as successful as its predecessor . The Channel Seven series was also filmed on location in Pitt Town, while, the Channel Ten series was filmed on location in Emerald, Victoria.",
    popularity: 13.042,
    poster_path: "/hxtsmmB1NsglgitpfmUMCQ2Cjnt.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/hxtsmmB1NsglgitpfmUMCQ2Cjnt.jpg",
    vote_average: 3,
    vote_count: 4
  },
  {
    backdrop_path: "/6GnHgJVVCFezvILU1mcx9X3W3AD.jpg",
    first_air_date: "2019-01-09",
    genre_ids: [35, 18],
    id: 85648,
    name: "Wanna Have A Good Time",
    origin_country: [],
    original_language: "en",
    original_name: "Wanna Have A Good Time",
    overview:
      "Shilpa plans to go to her maternal home. In her absence, her husband calls for a prostitute. When he looks at her face, she just looks like his own wife.",
    popularity: 24.359,
    poster_path: "/moCd79aZINa4OnLX9xhI2txCWH9.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/moCd79aZINa4OnLX9xhI2txCWH9.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/6GnHgJVVCFezvILU1mcx9X3W3AD.jpg",
    vote_average: 10,
    vote_count: 2
  },
  {
    backdrop_path: "/6JAt7phlR3kKYytHwOT8rPeag0U.jpg",
    first_air_date: "2013-04-23",
    genre_ids: [80, 18, 9648],
    id: 66627,
    name: "Murders in...",
    origin_country: ["FR"],
    original_language: "fr",
    original_name: "Meurtres à...",
    overview:
      "Murders in... is a collection of French-Belgian police TV movies taking place each time in a different French city and region.",
    popularity: 5.517,
    poster_path: "/9lLAZ3iOz8entXTgTNjooMqcRXu.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/9lLAZ3iOz8entXTgTNjooMqcRXu.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/6JAt7phlR3kKYytHwOT8rPeag0U.jpg",
    vote_average: 7.5,
    vote_count: 2
  },
  {
    backdrop_path: "/6piT539ZAaRKDmH4twqF3jEXGNi.jpg",
    first_air_date: "2016-10-24",
    genre_ids: [35],
    id: 67156,
    name: "Man with a Plan",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Man with a Plan",
    overview:
      "A dad finds out that parenting is harder than he thought after his wife goes back to work and he's left at home to take care of the kids.",
    popularity: 14.946,
    poster_path: "/scpvheiyBaBSi482ucSqJYH2ME1.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/scpvheiyBaBSi482ucSqJYH2ME1.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/6piT539ZAaRKDmH4twqF3jEXGNi.jpg",
    vote_average: 5.3,
    vote_count: 44
  },
  {
    backdrop_path: "/59UYt2nD7EJNpcgK1KD74jKJ1xy.jpg",
    first_air_date: "2018-10-12",
    genre_ids: [18],
    id: 81829,
    name: "Light as a Feather",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Light as a Feather",
    overview:
      "Five teen girls deal with the supernatural fallout stemming from an innocent game of “Light as a Feather, Stiff as a Board.” When the girls start dying off in the exact way that was predicted, the survivors must figure out why they’re being targeted — and whether the evil force hunting them down is one of their own.",
    popularity: 12.976,
    poster_path: "/xwX3TLo5eVHKAhX8pysq4cMQgi4.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/xwX3TLo5eVHKAhX8pysq4cMQgi4.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/59UYt2nD7EJNpcgK1KD74jKJ1xy.jpg",
    vote_average: 8.2,
    vote_count: 15
  },
  {
    backdrop_path: "/5DuK5TET80dSu3SufdHMvsX0P6B.jpg",
    first_air_date: "1998-03-10",
    genre_ids: [35],
    id: 75,
    name: "Two Guys and a Girl",
    origin_country: ["US"],
    original_language: "en",
    original_name: "Two Guys and a Girl",
    overview: "Two Guys and a Girl is an American sitcom",
    popularity: 10.789,
    poster_path: "/jFLDDn8XAOIv2sZ0aviiR7BSVbL.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/jFLDDn8XAOIv2sZ0aviiR7BSVbL.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/5DuK5TET80dSu3SufdHMvsX0P6B.jpg",
    vote_average: 7.2,
    vote_count: 60
  },
  {
    backdrop_path: "/9TyOYxzQr0SOmruw2i9F4vb1wXW.jpg",
    first_air_date: "2019-09-02",
    genre_ids: [80, 18],
    id: 93168,
    name: "A Confession",
    origin_country: ["GB"],
    original_language: "en",
    original_name: "A Confession",
    overview:
      "The story of how Detective Superintendent Steve Fulcher deliberately breached police procedure and protocol to catch a killer, a decision that ultimately cost him his career and reputation.",
    popularity: 5.393,
    poster_path: "/6c6q8m5PCiXv3TlxmM0vIcLylb0.jpg",
    poster_url:
      "https://image.tmdb.org/t/p/w185/6c6q8m5PCiXv3TlxmM0vIcLylb0.jpg",
    thumbnail_url:
      "https://image.tmdb.org/t/p/w1280/9TyOYxzQr0SOmruw2i9F4vb1wXW.jpg",
    vote_average: 8,
    vote_count: 2
  }
];
const Home = ({ suggestions, query }) => {
  return (
    <div
      style={{
        alignItems: "flex-start",
        paddingTop: "4rem",
        height: "calc(100vh - 4rem)",
        width: "100%",
        display: "flex",
        flexDirection: "column"
      }}
    >
      {suggestions.length ? (
        <React.Fragment>
          <Typography
            style={{ marginLeft: "10px" }}
            variant="h4"
            component="h4"
          >
            Search results for: "<b>{query}</b>"
          </Typography>
          <Slider>
            {suggestions.map(movie => (
              <Slider.Item serie={movie} key={movie.id}></Slider.Item>
            ))}
          </Slider>
        </React.Fragment>
      ) : query != "" ? (
        <React.Fragment>
          <Typography style={{ margin: "auto" }} variant="h5" component="h5">
            No result for: "<b>{query}</b>"
          </Typography>
        </React.Fragment>
      ) : (
        <React.Fragment>
          <Slider>
            {mockedSuggestions.map(movie => (
              <Slider.Item serie={movie} key={movie.id}></Slider.Item>
            ))}
          </Slider>
          <Slider>
            {mockedSuggestions.map(movie => (
              <Slider.Item serie={movie} key={movie.id}></Slider.Item>
            ))}
          </Slider>
        </React.Fragment>
      )}
    </div>
  );
};

const mapStateToProps = ({ suggestedSeries }) => {
  return {
    suggestions: suggestedSeries.suggestions,
    query: suggestedSeries.query
  };
};
export default connect(mapStateToProps)(Home);
