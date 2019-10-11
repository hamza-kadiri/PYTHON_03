import React, { useEffect, useState } from "react";
import { makeStyles } from '@material-ui/core/styles';
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button"
import LikeIcon from '@material-ui/icons/Favorite';
import OutlinedLikeIcon from '@material-ui/icons/FavoriteBorder';
import ky from "ky";

const useStyles = makeStyles(theme => ({
LikeIcon: {
  marginRight: theme.spacing(1),
},
}));



const Serie = ({ match }) => {
  const classes = useStyles();
  const [serie, setSerie] = useState({});
  const [isLiked, setisLiked] = useState(false)

  

  useEffect(() => {
    const getSerie = async id => {
      const response = await ky.get(`//localhost:8001/serie/${id}`);
      const json = await response.json();
      setSerie(json);
      return json;
    };
    getSerie(match.params.id);
  }, [match.params.id]);

  const handleLike = () => {
    const currentState = isLiked
    setisLiked(!currentState)
  }
  return (
    <React.Fragment>
      <div
        style={{
          background: "rgb(0, 0, 0)",
          backgroundImage: `linear-gradient(
                to right,
                rgba(0,0,0, 100) 15%,
                rgba(0,0,0, 0) 100%
              ), url(${serie.backdrop_url})`,
          backgroundSize: "cover",
          position: "absolute",
          height: "100vh",
          width: "100%",
          top: 0,
          zIndex: 1
        }}
      ></div>
      <div
        style={{
          position: "absolute",
          display: "flex",
          width: "100%",
          height: "100%",
          alignItems: "center",
          zIndex: 2
        }}
      >
        <Card
          elevation={0}
          style={{
            height: "80%",
            width: "25%",
            color: "white",
            background: `rgba(0,0,0,0)`
          }}
        >
          <CardContent>
            <Typography variant="h3" gutterBottom>
              {serie.name}
            </Typography>
            <Typography variant="body1" gutterBottom>
              {serie.overview}
            </Typography>
            <Button variant={isLiked ? "contained" : "outlined"} color="primary" onClick={handleLike}>
            {isLiked ? <LikeIcon className = {classes.LikeIcon}/> : <OutlinedLikeIcon className = {classes.LikeIcon}/>}
            Add to Favorites</Button>
          </CardContent>
        </Card>
      </div>
    </React.Fragment>
  );
};

export default Serie;
