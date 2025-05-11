import React, { useState } from "react";
import "./SettingPopup.scss";
import loginSubmitSystem from "../../services/loginSubmitSystem";
import loginUniqueInfor from "../../services/loginUniqueInfor";
import getLoginInfor from "../../services/getLoginInfor";
import {
  NotificationContainer,
  NotificationManager,
} from "react-notifications";
const SettingPopup = ({
  popupRef,
  listTranslateKey,
  currentTranslateKey,
  setCurrentTranslateKey,
}) => {
  const listSearchModel = {
    frame: "frame",
    video: "video",
    all: "all",
  };
  const [currentSearchModel, setCurrentSearchModel] = useState(
    listSearchModel.all
  );
  const [isOpenListTranslateKey, setIsOpenListTranslateKey] = useState(false);
  const [isOpenListSearchModel, setIsOpenListSearchModel] = useState(false);
  const [loginInfor, setLoginInfor] = useState({
    username: "",
    password: "",
  });
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLoginInfor((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const loginSubmit = async () => {
    if (loginInfor && loginInfor.username && loginInfor.password) {
      try {
        // const loginInforRes = await loginSubmitSystem(loginInfor);
        const loginInforRes = await loginUniqueInfor(loginInfor);
        if (loginInforRes) {
          console.log("LOGIN INFOR RES: ", loginInforRes);
          NotificationManager.success("Login successfully", "LOGIN", 3000);
        } else {
          NotificationManager.console.error("Cannot login!", "LOGIN", 3000);
        }
      } catch (e) {
        console.log("login error: ", e);
      }
    }
  };

  const loadLoginInfor = async () => {
    try {
      // const loginInforRes = await loginSubmitSystem(loginInfor);
      const loginInforRes = await getLoginInfor();
      if (loginInforRes) {
        console.log("LOGIN INFOR RES: ", loginInforRes);
        NotificationManager.success("Get login infor success", "LOGIN", 3000);
      } else {
        NotificationManager.console.error(
          "Cannot Get login infor!",
          "LOGIN",
          3000
        );
      }
    } catch (e) {
      console.log("Get login infor error: ", e);
    }
  };
  return (
    <div
      className="setting-popup"
      ref={popupRef}
      onClick={(e) => e.stopPropagation()} // Ngăn sự kiện mousedown lan ra ngoài
    >
      <div className="setting-item">
        <p className="setting-item__title">Translate Key</p>
        <div
          className="cus-select"
          onClick={(event) => {
            event.stopPropagation();
            setIsOpenListTranslateKey(!isOpenListTranslateKey);
            setIsOpenListSearchModel(false);
          }}
        >
          <p className="selection-name">
            Account{" "}
            {listTranslateKey.findIndex((key) => key === currentTranslateKey) +
              1}
          </p>
          <div className="drop-down">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g>
              <g id="SVGRepo_iconCarrier">
                <path
                  d="M11.1808 15.8297L6.54199 9.20285C5.89247 8.27496 6.55629 7 7.68892 7L16.3111 7C17.4437 7 18.1075 8.27496 17.458 9.20285L12.8192 15.8297C12.4211 16.3984 11.5789 16.3984 11.1808 15.8297Z"
                  fill="#33363F"
                ></path>
              </g>
            </svg>
          </div>
          {isOpenListTranslateKey && (
            <div className="list-selection">
              {listTranslateKey.map((key, index) => {
                return (
                  <p
                    className={`selection ${
                      currentTranslateKey === listTranslateKey[index]
                        ? "active-selection"
                        : null
                    }`}
                    key={index}
                    onClick={(e) => {
                      setCurrentTranslateKey(key);
                      e.stopPropagation();
                      setIsOpenListTranslateKey(false);
                    }}
                  >
                    Account {index + 1}
                  </p>
                );
              })}
            </div>
          )}
        </div>
      </div>
      <div className="setting-item">
        <p className="setting-item__title">Search Model</p>
        <div
          className="cus-select"
          onClick={(event) => {
            event.stopPropagation();
            setIsOpenListSearchModel(!isOpenListSearchModel);
            setIsOpenListTranslateKey(false);
          }}
        >
          <p className="selection-name">{currentSearchModel}</p>
          <div className="drop-down">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g>
              <g id="SVGRepo_iconCarrier">
                <path
                  d="M11.1808 15.8297L6.54199 9.20285C5.89247 8.27496 6.55629 7 7.68892 7L16.3111 7C17.4437 7 18.1075 8.27496 17.458 9.20285L12.8192 15.8297C12.4211 16.3984 11.5789 16.3984 11.1808 15.8297Z"
                  fill="#33363F"
                ></path>
              </g>
            </svg>
          </div>
          {isOpenListSearchModel && (
            <div className="list-selection">
              {Object.entries(listSearchModel).map(([key, value]) => (
                <p
                  className={`selection ${
                    currentSearchModel === value ? "active-selection" : null
                  }`}
                  key={key}
                  onClick={(e) => {
                    setCurrentSearchModel(value);
                    e.stopPropagation();
                    setIsOpenListSearchModel(false);
                  }}
                >
                  {value}
                </p>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="setting-item">
        <div className="login-services">
          <button className="login-button" onClick={loadLoginInfor}>
            GET INFOR
          </button>
          <button className="login-button" onClick={loginSubmit}>
            LOGIN
          </button>
        </div>
        <label htmlFor="username">
          User name:
          <input
            type="text"
            className="login-input"
            name="username"
            id="username"
            value={loginInfor.username}
            onChange={handleInputChange}
          />
        </label>
        <label htmlFor="username">
          Password:
          <input
            type="text"
            className="login-input"
            name="password"
            id="password"
            value={loginInfor.password}
            onChange={handleInputChange}
          />
        </label>
      </div>
    </div>
  );
};

export default SettingPopup;
