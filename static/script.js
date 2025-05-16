// Smooth scroll to "The Water-Climate Connection"
document.getElementById("learnMore").addEventListener("click", () => {
    document.getElementById("climate-connection").scrollIntoView({ behavior: "smooth" });
  });
  
  // Cycling facts
  const facts = [
    "Wastewater treatment plants are one of the largest industrial energy users in many cities.",
    "Proper treatment can reduce greenhouse gas emissions by over 50% in some facilities.",
    "The creator of this website should get an excellent, if not a perfect score on the assigment.",
    "In North America, over 20% of wastewater isn't treated properly.",
    "The amount of water on earth that can be used as drinking water is only around 1%.",
    "703 million people in the world - almost one in ten people don't have clean water close to home.",
    "Ancient civilizations like the Egyptians and Greeks used sand and gravel filters to purify water.",
    "The first modern water treatment plant was built in Scotland in 1804.",
    "Emerging contaminants like pharmaceuticals and microplastics pose new challenges for water treatment plants.",
    "A newborn baby is 78 percent water. Adults are 55-60 percent water.",
  ];
  
  let factIndex = 0;
  document.getElementById("show-fact").addEventListener("click", (e) => {
    e.preventDefault();
    factIndex = (factIndex + 1) % facts.length;
    document.getElementById("fact-text").textContent = facts[factIndex];
  });

/////////////////////////////////////////////////////////////
// USA slider
/////////////////////////////////////////////////////////////
  const slider = document.getElementById('treatment-slider');
  const currentRateEl = document.getElementById('current-rate');
  const sliderTargetRateEl = document.getElementById('slider-target-rate');
  const reductionTargetRateEl = document.getElementById('reduction-target-rate');
  const projectedCH4El = document.getElementById('projected-ch4');
  const projectedN2OEl = document.getElementById('projected-n2o');
  const reductionEl = document.getElementById('reduction');

  // Constants
  const baseCH4 = 157;
  const baseN2O = 11;
  const baseRate = 97;
  const targetMax = 100;
  // this value were calculates through a linear regression model based on the data 
  const targetCH4 = 150; 
  const targetN2O = 10.2;

  slider.addEventListener('input', () => {
    const rate = parseFloat(slider.value);
    const reductionRatio = (rate - baseRate) / (targetMax - baseRate);
  
    const projectedCH4 = (baseCH4 - (baseCH4 - targetCH4) * reductionRatio).toFixed(1);
    const projectedN2O = (baseN2O - (baseN2O - targetN2O) * reductionRatio).toFixed(1);
    const reductionPercent = ((1 - (projectedCH4 / baseCH4 + projectedN2O / baseN2O) / 2) * 100).toFixed(1);
  
    // Update UI
    currentRateEl.textContent = `${baseRate}%`;
    sliderTargetRateEl.textContent = `${rate}%`;
    reductionTargetRateEl.textContent = `${rate}%`;
    projectedCH4El.textContent = projectedCH4;
    projectedN2OEl.textContent = projectedN2O;
    reductionEl.textContent = `${reductionPercent}%`;
  });

/////////////////////////////////////////////////////////////
// Canada Slider
/////////////////////////////////////////////////////////////

const slider_can = document.getElementById('treatment-slider_can');
const currentRateEl_can = document.getElementById('current-rate_can');
const sliderTargetRateEl_can = document.getElementById('slider-target-rate_can');
const reductionTargetRateEl_can = document.getElementById('reduction-target-rate_can');
const projectedCH4El_can = document.getElementById('projected-ch4_can');
const projectedN2OEl_can = document.getElementById('projected-n2o_can');
const reductionEl_can = document.getElementById('reduction_can');

// Constants
const baseCH4_can = 15.4;
const baseN2O_can = 1.22;
const baseRate_can = 69;
const targetMax_can = 100;
// this value was calculated through a linear regression model based on the data of each country 
const targetCH4_can = 9.62;
const targetN2O_can = 0.71;

slider_can.addEventListener('input', () => {
  const rate_can = parseFloat(slider_can.value);
  const reductionRatio_can = (rate_can - baseRate_can) / (targetMax_can - baseRate_can);

  const projectedCH4_can = (baseCH4_can - (baseCH4_can - targetCH4_can) * reductionRatio_can).toFixed(1);
  const projectedN2O_can = (baseN2O_can - (baseN2O_can - targetN2O_can) * reductionRatio_can).toFixed(1);
  const reductionPercent_can = ((1 - (projectedCH4_can / baseCH4_can + projectedN2O_can / baseN2O_can) / 2) * 100).toFixed(1);

  // Update UI
  currentRateEl_can.textContent = `${baseRate_can}%`;
  sliderTargetRateEl_can.textContent = `${rate_can}%`;
  reductionTargetRateEl_can.textContent = `${rate_can}%`;
  projectedCH4El_can.textContent = projectedCH4_can;
  projectedN2OEl_can.textContent = projectedN2O_can;
  reductionEl_can.textContent = `${reductionPercent_can}%`;
});

/////////////////////////////////////////////////////////////
// Mexico Slider
/////////////////////////////////////////////////////////////

const slider_mex = document.getElementById('treatment-slider_mex');
const currentRateEl_mex = document.getElementById('current-rate_mex');
const sliderTargetRateEl_mex = document.getElementById('slider-target-rate_mex');
const reductionTargetRateEl_mex = document.getElementById('reduction-target-rate_mex');
const projectedCH4El_mex = document.getElementById('projected-ch4_mex');
const projectedN2OEl_mex = document.getElementById('projected-n2o_mex');
const reductionEl_mex = document.getElementById('reduction_mex');

// Constants for Mexico
const baseCH4_mex = 40.7;
const baseN2O_mex = 4.03;
const baseRate_mex = 64;
const targetMax_mex = 100;
// These values were calculated through a linear regression model based on the data 
const targetCH4_mex = 24.42;
const targetN2O_mex = 2.015;

slider_mex.addEventListener('input', () => {
  const rate = parseFloat(slider_mex.value);
  const reductionRatio = (rate - baseRate_mex) / (targetMax_mex - baseRate_mex);

  const projectedCH4 = (baseCH4_mex - (baseCH4_mex - targetCH4_mex) * reductionRatio).toFixed(1);
  const projectedN2O = (baseN2O_mex - (baseN2O_mex - targetN2O_mex) * reductionRatio).toFixed(1);
  const reductionPercent = ((1 - (projectedCH4 / baseCH4_mex + projectedN2O / baseN2O_mex) / 2) * 100).toFixed(1);

  // Update UI
  currentRateEl_mex.textContent = `${baseRate_mex}%`;
  sliderTargetRateEl_mex.textContent = `${rate}%`;
  reductionTargetRateEl_mex.textContent = `${rate}%`;
  projectedCH4El_mex.textContent = projectedCH4;
  projectedN2OEl_mex.textContent = projectedN2O;
  reductionEl_mex.textContent = `${reductionPercent}%`;
});
