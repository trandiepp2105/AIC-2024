function fuzzySearch(query, data) {
  // Chuyển query về chữ thường để không phân biệt chữ hoa chữ thường
  const lowerCaseQuery = query.toLowerCase();

  return data.reduce((matchingIndices, item, index) => {
    const lowerCaseItem = item.className.toLowerCase();
    if (fuzzyMatch(lowerCaseQuery, lowerCaseItem)) {
      matchingIndices.push(index);
    }
    return matchingIndices;
  }, []);
}

function fuzzyMatch(query, item) {
  let queryIndex = 0;
  let itemIndex = 0;

  while (queryIndex < query.length && itemIndex < item.length) {
    if (query[queryIndex] === item[itemIndex]) {
      queryIndex++;
    }
    itemIndex++;
  }

  return queryIndex === query.length;
}

export default fuzzySearch;
