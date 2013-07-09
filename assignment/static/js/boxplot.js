var lowerWhisker;
var q1;
var median;
var q3;
var upperWhisker;
var mildOutliers;
var extremeOutliers;
var min;
var max;

function sortNumber(a, b) {
	return a - b;
}

function calculateValues(data) {
	data.sort(sortNumber);
	var n = data.length;
	// lower quartile
	var q1Pos = (n * 0.25);
	if (q1Pos % 1 != 0) {
		q1Pos = Math.floor(q1Pos);
		q1 = data[q1Pos];
	} else {
		q1Pos = Math.floor(q1Pos);
		q1 = (data[q1Pos] + data[q1Pos-1]) / 2;
	}
	// median
	var medianPos = (n * 0.5);
	if (medianPos % 1 != 0) {
		medianPos = Math.floor(medianPos);
		median = data[medianPos];
	} else {
		medianPos = Math.floor(medianPos);
		median = (data[medianPos] + data[medianPos-1]) / 2;
	}
	// upper quartile
	var q3Pos = (n * 0.75);
	if (q3Pos % 1 != 0) {
		q3Pos = Math.floor(q3Pos);
		q3 = data[q3Pos];
	} else {
		q3Pos = Math.floor(q3Pos);
		q3 = (data[q3Pos] + data[q3Pos-1]) / 2;
	}	
	min = data[0];
	max = data[n - 1];
	
	var iqr = q3 - q1;
	mildOutliers = new Array();
	extremeOutliers = new Array();
	lowerWhisker = min;
	upperWhisker = max;
	if (min < (q1 - 1.5 * iqr)) {
		for (var i = 0; i < q1Pos; i++) {
			// we have to detect outliers
			if (data[i] < (q1 - 3 * iqr)) {
				extremeOutliers.push(data[i]);
			} else if (data[i] < (q1 - 1.5 * iqr)) {
				mildOutliers.push(data[i]);
			} else if (data[i] >= (q1 - 1.5 * iqr)) {
				lowerWhisker = data [i];
				break;
			}
		}
	}
	if (max > (q3 + (1.5 * iqr))) {
		for (i = q3Pos; i < data.length; i++) {
			// we have to detect outliers
			if (data[i] > (q3 + 3 * iqr)) {
				extremeOutliers.push(data[i]);
			} else if (data[i] > (q3 + 1.5 * iqr)) {
				mildOutliers.push(data[i]);
			} else if (data[i] <= (q3 + 1.5 * iqr)) {
				upperWhisker = data[i];
			}
		}
	}
}