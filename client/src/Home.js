import React from "react";
import Slider from "./Slider";
import { connect } from "react-redux";

import { fakeAuth } from "./App";

const Home = ({ suggestions }) => {
  console.log(suggestions);
  return (
    <div
      style={{
        alignItems: "flex-start",
        paddingTop: "8rem",
        height: "100%",
        width: "100%"
      }}
    >
      {suggestions.length && (
        <Slider>
          {suggestions.map(movie => (
            <Slider.Item serie={movie} key={movie.id}></Slider.Item>
          ))}
        </Slider>
      )}
    </div>
  );
};

const mapStateToProps = ({ suggestedSeries }) => {
  return {
    suggestions: suggestedSeries.suggestions
  };
};
export default connect(mapStateToProps)(Home);
