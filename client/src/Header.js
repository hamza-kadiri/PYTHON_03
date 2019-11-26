import { Button } from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import Avatar from "@material-ui/core/Avatar";
import Badge from "@material-ui/core/Badge";
import CircularProgress from "@material-ui/core/CircularProgress";
import IconButton from "@material-ui/core/IconButton";
import InputAdornment from "@material-ui/core/InputAdornment";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import { fade, makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import AccountCircle from "@material-ui/icons/AccountCircleOutlined";
import ClearIcon from "@material-ui/icons/ClearOutlined";
import MoreIcon from "@material-ui/icons/MoreVertOutlined";
import NotificationsIcon from "@material-ui/icons/NotificationsOutlined";
import SearchIcon from "@material-ui/icons/SearchOutlined";
import React, { useEffect, useState } from "react";
import Autosuggest from "react-autosuggest";
import { connect, useDispatch } from "react-redux";
import { NavLink, withRouter } from "react-router-dom";
import { Link } from "react-router-dom/";
import { userLogout } from "./actions/auth.actions";
import {
  getNotifications,
  markAsReadNotifications
} from "./actions/notifications.actions";
import {
  actions as seriesActions,
  fetchSuggestedSeries
} from "./actions/series.actions";
import { history } from "./helpers/history";

const useStyles = makeStyles(theme => {
  return {
    grow: {
      flexGrow: 1
    },
    menuButton: {
      marginRight: theme.spacing(2)
    },
    title: {
      display: "none",
      textShadow: "1px 1px 3px rgba(0,0,0,0.4)",
      [theme.breakpoints.up("sm")]: {
        display: "block"
      }
    },

    appBar: scrollY => ({
      backgroundColor: fade(
        theme.palette.common.black,
        Math.min(0.3 + scrollY / 10, 1)
      ),
      position: "fixed",
      zIndex: 10
    }),
    search: {
      position: "relative",
      borderRadius: theme.shape.borderRadius,
      opacity: 1,
      color: "black",
      backgroundColor: fade(theme.palette.common.white, 0.3),
      "&:hover": {
        backgroundColor: fade(theme.palette.common.white, 0.5)
      },
      marginRight: theme.spacing(2),
      marginLeft: 0,
      width: "70%",
      [theme.breakpoints.up("sm")]: {
        marginLeft: theme.spacing(3)
      }
    },

    sectionDesktop: {
      display: "none",
      [theme.breakpoints.up("md")]: {
        display: "flex"
      }
    },
    sectionMobile: {
      display: "flex",
      [theme.breakpoints.up("md")]: {
        display: "none"
      }
    },
    container: {
      position: "relative"
    },
    suggestionsContainerOpen: {
      position: "absolute",
      zIndex: 1,
      marginTop: theme.spacing(1),
      left: 0,
      right: 0
    },
    suggestion: {
      display: "block"
    },
    suggestionsList: {
      margin: 0,
      padding: 0,
      listStyleType: "none"
    },
    divider: {
      height: theme.spacing(2)
    },
    input: {
      color: theme.palette.common.white,
      paddingLeft: "10px"
    },
    suggestions: {
      root: {
        color: theme.palette.common.white
      }
    },
    inline: {
      display: "inline",
      color: fade(theme.palette.common.white, 0.7)
    },
    bigAvatar: {
      width: 55,
      height: 55,
      marginRight: 10
    }
  };
});

function PrimarySearchAppBar({
  suggestions,
  selectedSerie,
  suggestionQuery,
  user,
  notifications,
  scrollY
}) {
  const classes = useStyles(scrollY);
  const [anchorEl, setAnchorEl] = useState(null);
  const [notificationsAnchorEl, setNotificationsAnchorEl] = useState(null);
  const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = useState(null);
  const [value, setValue] = useState("");
  const [isLoadingSignout, setIsLoadingSignout] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    if (user.id) {
      dispatch(getNotifications(user.id));
    }
  }, [user, dispatch]);
  useEffect(() => {
    setValue(selectedSerie.serie.name);
  }, [selectedSerie]);

  const isMenuOpen = Boolean(anchorEl);
  const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);
  const isNotificationsOpen = Boolean(notificationsAnchorEl);

  const handleProfileMenuOpen = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleNotificationMenuOpen = event => {
    setNotificationsAnchorEl(event.currentTarget);
  };

  const handleMobileMenuClose = () => {
    setMobileMoreAnchorEl(null);
  };

  const handleSignout = async () => {
    setIsLoadingSignout(true);
    dispatch(userLogout());
    setIsLoadingSignout(false);
    handleMenuClose();
  };

  const handleFavorites = async () => {
    handleMenuClose();
    history.push("/favorites");
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    handleMobileMenuClose();
  };

  const handleNotificationsClose = () => {
    setNotificationsAnchorEl(null);
    dispatch(markAsReadNotifications(user.id, notifications));
  };

  const handleMobileMenuOpen = event => {
    setMobileMoreAnchorEl(event.currentTarget);
  };

  const menuId = "primary-search-account-menu";
  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      id={menuId}
      keepMounted
      transformOrigin={{ vertical: "top", horizontal: "right" }}
      open={isMenuOpen}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={handleFavorites}>Favorites</MenuItem>
      <MenuItem onClick={handleSignout}>
        {isLoadingSignout ? (
          <ListItemIcon>
            <CircularProgress style={{ margin: "auto" }} size={24} />
          </ListItemIcon>
        ) : (
          "Sign out"
        )}
      </MenuItem>
    </Menu>
  );

  const renderSerieNotification = (notification, index) => (
    <MenuItem
      component={Link}
      to={`/serie/${notification.tmdb_id_serie}`}
      key={`notification-${index}`}
      alignItems="flex-start"
    >
      <ListItemAvatar>
        <Badge
          color="primary"
          anchorOrigin={{
            horizontal: "left",
            vertical: "top"
          }}
          overlap="circle"
          badgeContent=" "
          invisible={notification.read}
        >
          <Avatar src={notification.poster_url} className={classes.bigAvatar} />
        </Badge>
      </ListItemAvatar>
      <ListItemText
        primary={
          <Typography>
            {notification.serie_name} —{" "}
            {new Date(notification.next_air_date).toLocaleDateString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric"
            })}
          </Typography>
        }
        secondary={
          <React.Fragment>
            <Typography
              component="span"
              variant="body2"
              className={classes.inline}
            >
              Season : {notification.season_number} - Episode{" "}
              {notification.episode_number}
            </Typography>{" "}
          </React.Fragment>
        }
      />
    </MenuItem>
  );
  const renderNotifications = notifications.length > 0 && (
    <Menu
      anchorEl={notificationsAnchorEl}
      id={menuId}
      keepMounted
      transformOrigin={{ vertical: "bottom", horizontal: "left" }}
      open={isNotificationsOpen}
      onClose={handleNotificationsClose}
    >
      {notifications
        .filter(notification => notification.next_air_date != null)
        .map((notification, index) => {
          return renderSerieNotification(notification, index);
        })}
    </Menu>
  );

  const mobileMenuId = "primary-search-account-menu-mobile";
  const renderMobileMenu = (
    <Menu
      anchorEl={mobileMoreAnchorEl}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      id={mobileMenuId}
      keepMounted
      transformOrigin={{ vertical: "top", horizontal: "right" }}
      open={isMobileMenuOpen}
      onClose={handleMobileMenuClose}
    >
      <MenuItem onClick={handleNotificationMenuOpen}>
        <IconButton color="inherit">
          <Badge
            color="secondary"
            invisible={
              notifications.filter(
                notification =>
                  notification.read === false &&
                  notification.next_air_date != null
              ).length === 0
            }
            badgeContent={
              <Typography color="textPrimary" variant="caption">
                {
                  notifications.filter(
                    notification =>
                      notification.read === false &&
                      notification.next_air_date != null
                  ).length
                }
              </Typography>
            }
          >
            <NotificationsIcon />
          </Badge>
        </IconButton>
        Notifications
      </MenuItem>
      <MenuItem onClick={handleProfileMenuOpen}>
        <IconButton
          aria-label="account of current user"
          aria-controls="primary-search-account-menu"
          aria-haspopup="true"
          color="inherit"
        >
          <AccountCircle />
        </IconButton>
        <p>Profile</p>
      </MenuItem>
    </Menu>
  );

  const getOptionValue = option => {
    return option.name;
  };

  const loadSuggestions = async inputValue => {
    await dispatch(fetchSuggestedSeries(inputValue));
    return suggestions;
  };

  const onSuggestionsFetchRequested = async ({ value }) => {
    await loadSuggestions(value);
  };

  const clearSuggestions = () => {
    dispatch({
      type: seriesActions.RESET_SUGGESTED_SERIES
    });
    history.push("/");
    setValue("");
  };

  const onChange = (event, { newValue }) => {
    setValue(newValue);
    history.push("/");
  };

  function renderInputComponent(inputProps) {
    const { classes, inputRef = () => {}, ref, ...other } = inputProps;
    return (
      <TextField
        fullWidth
        InputProps={{
          inputRef: node => {
            ref(node);
            inputRef(node);
          },
          className: classes.input,
          endAdornment: (
            <InputAdornment position="end">
              {value === "" ? (
                <IconButton className={classes.input} aria-label="search">
                  <SearchIcon />
                </IconButton>
              ) : (
                <IconButton
                  onClick={clearSuggestions}
                  className={classes.input}
                  aria-label="search"
                >
                  <ClearIcon />
                </IconButton>
              )}
            </InputAdornment>
          )
        }}
        {...other}
      />
    );
  }

  function renderSuggestion(suggestion, { query, isHighlighted }) {
    return null;
  }

  const onSuggestionSelected = (event, { suggestion }) => {
    if (event.key === "Enter") {
      const path = `/serie/${suggestion.id}`;
      history.push(path);
    }
  };

  const inputProps = {
    placeholder: "Search a serie",
    value,
    onChange,
    classes
  };
  return (
    <div className={classes.grow}>
      <AppBar className={classes.appBar}>
        {localStorage.getItem("user") && (
          <Toolbar style={{ color: "white" }}>
            <Button
              style={{ textTransform: "none" }}
              component={NavLink}
              to="/"
            >
              <Typography className={classes.title} variant="h6" noWrap>
                Favorite Series
              </Typography>
            </Button>
            <div className={classes.search}>
              <Autosuggest
                suggestions={suggestions}
                alwaysRenderSuggestions={true}
                onSuggestionsFetchRequested={onSuggestionsFetchRequested}
                onSuggestionSelected={onSuggestionSelected}
                getSuggestionValue={getOptionValue}
                renderInputComponent={renderInputComponent}
                renderSuggestion={renderSuggestion}
                inputProps={inputProps}
                theme={{
                  container: classes.container,
                  suggestionsContainerOpen: classes.suggestionsContainerOpen,
                  suggestionsList: classes.suggestionsList,
                  suggestion: classes.suggestion
                }}
              />
            </div>
            <div className={classes.grow} />
            <div className={classes.sectionDesktop}>
              <IconButton onClick={handleNotificationMenuOpen} color="inherit">
                <Badge
                  color="secondary"
                  invisible={
                    notifications.filter(
                      notification =>
                        notification.read === false &&
                        notification.next_air_date != null
                    ).length === 0
                  }
                  badgeContent={
                    <Typography color="textPrimary" variant="caption">
                      {
                        notifications.filter(
                          notification =>
                            notification.read === false &&
                            notification.next_air_date != null
                        ).length
                      }
                    </Typography>
                  }
                >
                  <NotificationsIcon />
                </Badge>
              </IconButton>
              <IconButton
                edge="end"
                aria-label="account of current user"
                aria-controls={menuId}
                aria-haspopup="true"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
            </div>
            <div className={classes.sectionMobile}>
              <IconButton
                aria-label="show more"
                aria-controls={mobileMenuId}
                aria-haspopup="true"
                onClick={handleMobileMenuOpen}
                color="inherit"
              >
                <MoreIcon />
              </IconButton>
            </div>
          </Toolbar>
        )}
      </AppBar>
      {renderMobileMenu}
      {renderMenu}
      {renderNotifications}
    </div>
  );
}

const mapStateToProps = ({
  suggestedSeries,
  selectedSerie,
  user,
  notifications
}) => {
  return {
    suggestions: suggestedSeries.suggestions,
    suggestionQuery: suggestedSeries.query,
    selectedSerie: selectedSerie,
    user: user.user,
    notifications: notifications.notifications
  };
};
export default connect(mapStateToProps)(withRouter(PrimarySearchAppBar));
