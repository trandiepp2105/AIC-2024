function fuzzySearch(query, data) {
  // Chuyển query về chữ thường để không phân biệt chữ hoa chữ thường
  const lowerCaseQuery = query.toLowerCase();

  return data.filter((item) => {
    const lowerCaseItem = item.toLowerCase();
    return fuzzyMatch(lowerCaseQuery, lowerCaseItem);
  });
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
