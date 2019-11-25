import { Typography, CircularProgress } from "@material-ui/core";
import React, { useEffect } from "react";
import { connect, useDispatch } from "react-redux";
import Slider from "./Slider";
import { getDiscoverSeries } from "./actions/series.actions";

const Home = ({ suggestions, query, categories, isFetching }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(getDiscoverSeries());
  }, [dispatch]);
  return (
    <div
      style={{
        alignItems: "flex-start",
        paddingTop: "4rem",
        height: "calc(100vh - 4rem)",
        width: "100%",
        flexDirection: "column"
      }}
    >
      {suggestions.length ? (
        <React.Fragment>
          <Typography
            style={{
              paddingLeft: "10px",
              fontSize: "42px",
              paddingTop: "10px"
            }}
            variant="h4"
            component="h4"
          >
            Search results for: "<b>{query}</b>"
          </Typography>
          <Slider singleSlider>
            {suggestions.map(movie => (
              <Slider.Item serie={movie} key={movie.id}></Slider.Item>
            ))}
          </Slider>
        </React.Fragment>
      ) : query !== "" ? (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%"
          }}
        >
          <Typography variant="h5" component="h5">
            No result for: "<b>{query}</b>"
          </Typography>
        </div>
      ) : isFetching ? (
        <CircularProgress
          style={{
            position: "absolute",
            margin: "auto",
            left: 0,
            right: 0,
            top: 0,
            bottom: 0
          }}
          size={50}
          color="primary"
        />
      ) : (
        categories.map((category, index) => {
          return (
            <React.Fragment key={`category-${index}`}>
              <Typography
                variant="h4"
                style={{
                  fontSize: "42px",
                  color: "#fff",
                  fontWeight: "1000",
                  paddingLeft: "10px",
                  paddingTop: "10px"
                }}
              >
                {category.name}
              </Typography>
              <Slider>
                {category.series.map(serie => (
                  <Slider.Item serie={serie} key={serie.id}></Slider.Item>
                ))}
              </Slider>
            </React.Fragment>
          );
        })
      )}
    </div>
  );
};

const mapStateToProps = ({ suggestedSeries, discoverSeries }) => {
  return {
    suggestions: suggestedSeries.suggestions,
    query: suggestedSeries.query,
    categories: discoverSeries.categories,
    isFetching: discoverSeries.isFetching
  };
};
export default connect(mapStateToProps)(Home);
