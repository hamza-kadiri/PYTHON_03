import clientWeb from "../helpers/clientWeb";
import { history } from "../helpers/history";
import { handleError } from "./common.actions";

export const actions = {
  REQUEST_GET_NOTIFICATIONS: "REQUEST_NOTIFICATIONS",
  SUCCESS_GET_NOTIFICATIONS: "SUCCESS_NOTIFICATIONS",
  ERROR_GET_NOTIFICATIONS: "ERROR_NOTIFICATIONS",
  REQUEST_MARK_AS_READ_: "REQUEST_MARK_AS_READ",
  SUCCESS_MARK_AS_READ: "SUCCESS_MARK_AS_READ",
  ERROR_MARK_AS_READ: "ERROR_MARK_AS_READ"
};

const requestNotifications = (actionType, user_id) => {
  return {
    type: actionType,
    user_id
  };
};

const receiveNotifications = (actionType, response) => {
  return {
    type: actionType,
    notifications: response.notifications
  };
};

export const getNotifications = user_id => {
  return async dispatch => {
    try {
      await dispatch(
        requestNotifications(actions.REQUEST_GET_NOTIFICATIONS, user_id)
      );
      const response = await clientWeb(`users/${user_id}/notifications`);
      const json = await response.json();
      await dispatch(
        receiveNotifications(actions.SUCCESS_GET_NOTIFICATIONS, json)
      );
    } catch (error) {
      dispatch(handleError(error, actions.ERROR_GET_NOTIFICATIONS));
    }
  };
};
