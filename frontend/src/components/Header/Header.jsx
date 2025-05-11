import React from "react";
import "./Header.scss";
const Header = () => {
  return (
    <div className="header">
      {/* <h2 className="header-title">VIDEO BROWSER APPLICATION</h2> */}
      <div className="logo">
        <img
          className="logo-img"
          src={`${process.env.PUBLIC_URL}/logo_cua_huu.png`}
          alt="Logo"
        />
      </div>
      <p className="team-name">Tứ Đại Thạch Hầu</p>
    </div>
  );
};

export default Header;
