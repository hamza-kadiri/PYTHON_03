import React from "react";
import Slider from "./Slider";
import { connect } from "react-redux";

import { fakeAuth } from "./App";
import { Typography } from "@material-ui/core";

const Home = ({ suggestions }) => {
  console.log(suggestions);
  return (
    <div
      style={{
        alignItems: "flex-start",
        paddingTop: "4rem",
        height: "calc(100vh - 4rem)",
        width: "100%"
      }}
    >
      {suggestions.length ? (
        <React.Fragment>
          <Typography variant="h4" component="h4">
            {" "}
            Search results for:{" "}
          </Typography>
          <Slider>
            {suggestions.map(movie => (
              <Slider.Item serie={movie} key={movie.id}></Slider.Item>
            ))}
          </Slider>{" "}
        </React.Fragment>
      ) : null}
    </div>
  );
};

const mapStateToProps = ({ suggestedSeries }) => {
  return {
    suggestions: suggestedSeries.suggestions
  };
};
export default connect(mapStateToProps)(Home);
