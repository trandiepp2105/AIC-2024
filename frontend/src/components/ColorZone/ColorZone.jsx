import React from "react";
import "./ColorZone.scss";

const ColorZone = ({ searchData, setSearchData, currentColor }) => {
  const handleChangeColorTable = (rowIndex, colIndex) => {
    setSearchData((prevData) => {
      const newSearchData = {
        ...prevData,
        colors: {
          ...prevData.colors,
          value: {
            ...prevData.colors.value,
            table: prevData.colors.value.table.map((row, rIdx) =>
              row.map((col, cIdx) => {
                if (rIdx === rowIndex && cIdx === colIndex) {
                  return currentColor;
                }
                return col;
              })
            ),
          },
        },
      };
      return newSearchData;
    });
  };
  // Tạo một mảng để lưu trữ các hàng
  const rowStyle = {
    height: `calc(100% / ${searchData.colors.value.row})`,
  };

  const cellStyle = (backgroundColor) => ({
    width: `calc(100% / ${searchData.colors.value.column})`,
    backgroundColor: backgroundColor,
  });

  const rows = Array.from(
    { length: searchData.colors.value.row },
    (_, rowIndex) => {
      // Mỗi hàng chứa một mảng các ô
      const columns = Array.from(
        { length: searchData.colors.value.column },
        (_, colIndex) => (
          <div
            key={`col-${colIndex}`}
            className="cell"
            style={cellStyle(searchData.colors.value.table[rowIndex][colIndex])}
            onClick={() => {
              handleChangeColorTable(rowIndex, colIndex, currentColor);
            }}
          ></div>
        )
      );

      return (
        <div key={`row-${rowIndex}`} className="row" style={rowStyle}>
          {columns}
        </div>
      );
    }
  );

  return <div className="color-zone-picker">{rows}</div>;
};

export default ColorZone;
