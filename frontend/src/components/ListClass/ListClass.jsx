import React, { useState, useEffect, useRef } from "react";
import "./ListClass.scss";

function swap(array, index1, index2) {
  let temp = array[index1];
  array[index1] = array[index2];
  array[index2] = temp;
}

const ListClass = ({ classes, setClasses, setSearchData, width = "" }) => {
  const [activeClass, setActiveClass] = useState(null);
  const inputRefs = useRef([]);
  const firstInputRef = useRef(null);
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
      // if (firstInputRef.current) {
      //   firstInputRef.current.focus();
      // }
      if (inputRefs.current[0]) {
        inputRefs.current[0].focus();
      }
      setActiveClass(0);
    }
  }, [isAddIncQuantity]);

  const handleChangeQuantity = (index, event) => {
    setIsAddIncQuantity(false);
    const newQuantity = event.target.value;
    const quantityInt = parseInt(newQuantity, 10);
    setClasses((prevClasses) => {
      const newClasses = [...prevClasses];
      newClasses[index].quantity = newQuantity;

      if (!isNaN(quantityInt) && quantityInt > 0) {
        const temp = newClasses[index];
        for (let i = index; i > 0; i--) {
          newClasses[i] = newClasses[i - 1];
        }
        newClasses[0] = temp;
        setIsAddIncQuantity(true);
      } else {
        for (let i = index; i < newClasses.length - 1; i++) {
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
        (obj) => obj.className === classes[index].className
      );

      if (existingObjectIndex !== -1) {
        if (quantityInt === 0 || isNaN(quantityInt)) {
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
        } else {
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
        }
      } else {
        if (quantityInt > 0) {
          return {
            ...prevData,
            objects: {
              ...prevData.objects,
              value: [
                ...prevData.objects.value,
                { className: classes[index].className, quantity: quantityInt },
              ],
            },
          };
        }
      }

      return prevData;
    });
  };

  return (
    <ul className="list-class" style={{ width }}>
      {classes.map((value, index) => (
        <li
          key={`class-item-${index}`}
          className={`class-item ${
            activeClass === index ? "active-item" : ""
          } ${
            !isNaN(parseInt(value.quantity, 10)) &&
            parseInt(value.quantity, 10) > 0
              ? "chosen-item"
              : null
          }`}
          onClick={() => handleItemClick(index)}
        >
          <p>{value.className}</p>
          <input
            type="number"
            min={0}
            name={`class-item-quantity-${index}`}
            className="class-item-quantity"
            value={value.quantity}
            onChange={(event) => handleChangeQuantity(index, event)}
            // ref={index === 0 ? firstInputRef : null}
            ref={(el) => (inputRefs.current[index] = el)}
          />
        </li>
      ))}
    </ul>
  );
};

export default ListClass;
