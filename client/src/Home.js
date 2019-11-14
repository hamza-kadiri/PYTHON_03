import { Typography } from "@material-ui/core";
import React from "react";
import { connect } from "react-redux";
import Slider from "./Slider";

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
            Search results for: <b>{query}</b>
          </Typography>
          <Slider>
            {suggestions.map(movie => (
              <Slider.Item serie={movie} key={movie.id}></Slider.Item>
            ))}
          </Slider>
        </React.Fragment>
      ) : null}
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
