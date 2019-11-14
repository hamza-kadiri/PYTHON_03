import AppBar from "@material-ui/core/AppBar";
import Badge from "@material-ui/core/Badge";
import CircularProgress from "@material-ui/core/CircularProgress";
import IconButton from "@material-ui/core/IconButton";
import InputAdornment from "@material-ui/core/InputAdornment";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import { fade, makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import AccountCircle from "@material-ui/icons/AccountCircleOutlined";
import MenuIcon from "@material-ui/icons/MenuOutlined";
import MoreIcon from "@material-ui/icons/MoreVertOutlined";
import NotificationsIcon from "@material-ui/icons/NotificationsOutlined";
import SearchIcon from "@material-ui/icons/SearchOutlined";
import React, { useEffect, useState } from "react";
import Autosuggest from "react-autosuggest";
import { connect, useDispatch } from "react-redux";
import { history } from "./helpers/history";
import { withRouter } from "react-router-dom";
import { fetchSuggestedSeries } from "./actions/series.actions";
import { userLogout } from "./actions/user.actions";

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

    appBar: {
      backgroundColor: fade(theme.palette.primary.main, 0.05),
      position: "fixed",
      zIndex: 10
    },
    search: {
      position: "relative",
      borderRadius: theme.shape.borderRadius,
      opacity: 1,
      backgroundColor: fade(theme.palette.common.white, 0.15),
      "&:hover": {
        backgroundColor: fade(theme.palette.common.white, 0.25)
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
      color: theme.palette.common.white
    },
    suggestions: {
      root: {
        color: theme.palette.common.white
      }
    }
  };
});

function PrimarySearchAppBar({ suggestions, selectedSerie }) {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = useState(null);
  const [value, setValue] = useState("");
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [isLoadingSignout, setIsLoadingSignout] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    setValue(selectedSerie.serie.name);
  }, [selectedSerie]);

  const isMenuOpen = Boolean(anchorEl);
  const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);

  const handleProfileMenuOpen = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleMobileMenuClose = () => {
    setMobileMoreAnchorEl(null);
  };

  const handleSignout = async () => {
    setIsLoadingSignout(true);
    dispatch(userLogout());
    setIsLoadingSignout(false);
    handleMenuClose();
    history.push("/login");
  };

  const handleFavorites = async () => {
    handleMenuClose();
    history.push("/favorites");
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    handleMobileMenuClose();
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
      <MenuItem>
        <IconButton aria-label="show 11 new notifications" color="inherit">
          <Badge badgeContent={11} color="secondary">
            <NotificationsIcon />
          </Badge>
        </IconButton>
        <p>Notifications</p>
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

  const onSuggestionsClearRequested = () => {};

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
              {isLoadingSuggestions ? (
                <IconButton className={classes.input} aria-label="search">
                  <CircularProgress size={16} />
                </IconButton>
              ) : (
                <IconButton className={classes.input} aria-label="search">
                  <SearchIcon />
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
    placeholder: "Rechercher une série",
    value,
    onChange,
    classes
  };
  return (
    <div className={classes.grow}>
      <AppBar className={classes.appBar}>
        {localStorage.getItem("user") && (
          <Toolbar style={{ color: "white" }}>
            <IconButton
              edge="start"
              className={classes.menuButton}
              color="inherit"
              aria-label="open drawer"
            >
              <MenuIcon />
            </IconButton>
            <Typography className={classes.title} variant="h6" noWrap>
              Séries Préférées
            </Typography>
            <div className={classes.search}>
              <Autosuggest
                highlightFirstSuggestion
                suggestions={suggestions}
                onSuggestionsFetchRequested={onSuggestionsFetchRequested}
                onSuggestionsClearRequested={onSuggestionsClearRequested}
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
              <IconButton
                aria-label="show 17 new notifications"
                color="inherit"
              >
                <Badge badgeContent={17} color="secondary">
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
    </div>
  );
}

const mapStateToProps = ({ suggestedSeries, selectedSerie }) => {
  return {
    suggestions: suggestedSeries.suggestions,
    selectedSerie: selectedSerie
  };
};
export default connect(mapStateToProps)(withRouter(PrimarySearchAppBar));
