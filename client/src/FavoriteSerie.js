import React, { useState } from "react";
import Slider from "./Slider";
import Typography from "@material-ui/core/Typography";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import FormControl from "@material-ui/core/FormControl";
import { Grid } from "@material-ui/core";

const FavoriteSerie = ({ serie }) => {
  const [season, setSeason] = useState(0);
  const handleChange = event => {
    setSeason(event.target.value);
  };
  const seasons = serie.seasons;
  return seasons ? (
    <React.Fragment key={serie.id}>
      <Grid
        container
        style={{
          paddingLeft: "10px",
          paddingTop: "10px",
          width: "90%"
        }}
        alignItems="center"
        spacing={2}
      >
        <Grid item>
          <Typography
            variant="h4"
            style={{
              fontSize: "42px",
              color: "#fff",
              fontWeight: "1000"
            }}
          >
            {serie.name}
          </Typography>
        </Grid>
        <Grid item>
          <FormControl style={{ minWidth: "120px" }}>
            <Select
              style={{
                fontSize: "32px",
                fontWeight: "700"
              }}
              value={season}
              onChange={handleChange}
            >
              {seasons.map((season, index) => (
                <MenuItem key={index} value={index}>
                  {season.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>
      <Slider episode>
        {serie.seasons[season].episodes.map((episode, index) => {
          episode["id"] = `${serie.id}-${index}`;
          return (
            <Slider.Item episode serie={episode} key={episode.id}></Slider.Item>
          );
        })}
      </Slider>
    </React.Fragment>
  ) : null;
};

export default FavoriteSerie;
