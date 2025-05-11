import React, { useState, useEffect, useRef } from "react";
import "./ListClass.scss";

function swap(array, index1, index2) {
  let temp = array[index1];
  array[index1] = array[index2];
  array[index2] = temp;
}

const ListClass = ({
  classes,
  setClasses,
  setSearchData,
  classesIndexDisplay,
  setClassesIndexDisplay,
  width = "",
}) => {
  const [activeClass, setActiveClass] = useState(null);
  const inputRefs = useRef([]);
  const [isAddIncQuantity, setIsAddIncQuantity] = useState(false);

  const handleItemClick = (index) => {
    setActiveClass(index);
  };

  const handleOutsideClick = (event) => {
    if (!event.target.closest(".class-item")) {
      setActiveClass(null);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleOutsideClick);
    return () => {
      document.removeEventListener("click", handleOutsideClick);
    };
  }, []);

  useEffect(() => {
    if (isAddIncQuantity === true) {
      if (inputRefs.current[0]) {
        inputRefs.current[0].focus();
      }
      setActiveClass(0);
    }
  }, [isAddIncQuantity]);

  const handleChangeQuantity = (indexClasses, index, event) => {
    setIsAddIncQuantity(false);
    const newQuantity = event.target.value;
    const quantityInt = parseInt(newQuantity, 10);

    setClasses((prevClasses) => {
      const newClasses = [...prevClasses];
      newClasses[indexClasses].quantity = newQuantity;

      if (!isNaN(quantityInt) && quantityInt > 0) {
        const temp = newClasses[indexClasses];
        for (let i = indexClasses; i > 0; i--) {
          newClasses[i] = newClasses[i - 1];
        }
        newClasses[0] = temp;
        setIsAddIncQuantity(true);

        // Cập nhật lại classesIndexDisplay
        setClassesIndexDisplay((preIndex) => {
          const newIndex = preIndex.map((_, i) => i);
          return newIndex;
        });
      } else if (quantityInt === 0) {
        // Giữ nguyên thứ tự khi quantity = 0
      } else {
        for (let i = indexClasses; i < newClasses.length - 1; i++) {
          const nextQuantity = parseInt(newClasses[i + 1].quantity, 10);
          if (isNaN(nextQuantity) || nextQuantity <= 0) {
            break;
          }
          swap(newClasses, i, i + 1);
          if (inputRefs.current[i + 1]) {
            inputRefs.current[i + 1].focus();
          }
          setActiveClass(i + 1);
        }
      }
      return newClasses;
    });

    setSearchData((prevData) => {
      const existingObjectIndex = prevData.objects.value.findIndex(
        (obj) => obj.className === classes[indexClasses].className
      );

      if (existingObjectIndex !== -1) {
        if (quantityInt > 0) {
          const updatedValue = prevData.objects.value.map((obj, i) =>
            i === existingObjectIndex ? { ...obj, quantity: quantityInt } : obj
          );
          return {
            ...prevData,
            objects: {
              ...prevData.objects,
              value: updatedValue,
            },
          };
        } else {
          const updatedValue = prevData.objects.value.filter(
            (_, i) => i !== existingObjectIndex
          );
          return {
            ...prevData,
            objects: {
              ...prevData.objects,
              value: updatedValue,
            },
          };
        }
      } else if (quantityInt > 0) {
        return {
          ...prevData,
          objects: {
            ...prevData.objects,
            value: [
              ...prevData.objects.value,
              {
                className: classes[indexClasses].className,
                quantity: quantityInt,
              },
            ],
          },
        };
      }

      return prevData;
    });
  };

  return (
    <ul className="list-class" style={{ width }}>
      {classesIndexDisplay.map((indexClasses, index) => (
        <li
          key={`class-item-${indexClasses}`}
          className={`class-item ${
            activeClass === indexClasses ? "active-item" : ""
          } ${
            !isNaN(parseInt(classes[indexClasses].quantity, 10)) &&
            parseInt(classes[indexClasses].quantity, 10) > 0
              ? "chosen-item"
              : null
          }`}
          onClick={() => handleItemClick(indexClasses)}
        >
          <p>{classes[indexClasses].className}</p>
          <input
            type="number"
            min={0}
            name={`class-item-quantity-${indexClasses}`}
            className="class-item-quantity"
            value={classes[indexClasses].quantity}
            onChange={(event) =>
              handleChangeQuantity(indexClasses, index, event)
            }
            ref={(el) => (inputRefs.current[index] = el)}
          />
        </li>
      ))}
    </ul>
  );
};

export default ListClass;
