/**
 * Sorts a HTML table.
 *
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending
 * @param {columnHeadText} headtext Determines the name of the colume, to identify if float has to be parsed
 */
function sortTableByColumn(table, column, headtext, asc = true) {
	const dirModifier = asc ? 1 : -1;
	const tBody = table.tBodies[0];
	const rows = Array.from(tBody.querySelectorAll("tr"));

	// Sort each row
	if (headtext == "Price"){
		const sortedRows = rows.sort((a, b) => {
			const aColFloat = parseFloat(a.querySelector(`td:nth-child(${column + 1})`).textContent.trim());
			const bColFloat = parseFloat(b.querySelector(`td:nth-child(${column + 1})`).textContent.trim());
			return aColFloat > bColFloat ? (1 * dirModifier) : (-1 * dirModifier);
		});
			// Remove all existing TRs from the table
		while (tBody.firstChild) {
			tBody.removeChild(tBody.firstChild);
		}

		// Re-add the newly sorted rows
		tBody.append(...sortedRows);
	}
	else {
		const sortedRows = rows.sort((a, b) => {
			const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
			const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
			return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
		});
			// Remove all existing TRs from the table
		while (tBody.firstChild) {
			tBody.removeChild(tBody.firstChild);
		}

		// Re-add the newly sorted rows
		tBody.append(...sortedRows);
	}



	// Remember how the column is currently sorted
	table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
	table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
	table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".stonks_table_sortable th").forEach(headerCell => {
	headerCell.addEventListener("click", () => {
		const tableElement = headerCell.parentElement.parentElement.parentElement;
		const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
		const currentIsAscending = headerCell.classList.contains("th-sort-asc");
		const columnHeadText = headerCell.textContent;

		sortTableByColumn(tableElement, headerIndex, columnHeadText, !currentIsAscending);
	});
});