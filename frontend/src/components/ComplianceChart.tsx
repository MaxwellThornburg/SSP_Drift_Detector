// frontend/src/components/ComplianceChart.tsx

import React from 'react';

interface ComplianceData {
  compliant: number;
  nonCompliant: number;
  notImplemented: number;
  compliancePercentage: number;
}

interface ComplianceChartProps {
  data: ComplianceData;
}

const ComplianceChart: React.FC<ComplianceChartProps> = ({ data }) => {
  const { compliant, nonCompliant, notImplemented, compliancePercentage } = data;
  const total = compliant + nonCompliant + notImplemented;

  // Calculate pie chart segments
  const compliantAngle = (compliant / total) * 360;
  const nonCompliantAngle = (nonCompliant / total) * 360;
  
  // SVG path calculations for pie slices
  const getPieSlice = (startAngle: number, endAngle: number, radius: number = 80) => {
    const startRad = (startAngle - 90) * (Math.PI / 180);
    const endRad = (endAngle - 90) * (Math.PI / 180);
    
    const x1 = 100 + radius * Math.cos(startRad);
    const y1 = 100 + radius * Math.sin(startRad);
    const x2 = 100 + radius * Math.cos(endRad);
    const y2 = 100 + radius * Math.sin(endRad);
    
    const largeArc = endAngle - startAngle > 180 ? 1 : 0;
    
    return `M 100 100 L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2} Z`;
  };

  let currentAngle = 0;
  const compliantSlice = getPieSlice(currentAngle, currentAngle + compliantAngle);
  currentAngle += compliantAngle;
  const nonCompliantSlice = getPieSlice(currentAngle, currentAngle + nonCompliantAngle);
  currentAngle += nonCompliantAngle;
  const notImplementedSlice = getPieSlice(currentAngle, currentAngle + ((notImplemented / total) * 360));

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        {/* Pie Chart SVG */}
        <svg width="200" height="200" className="transform -rotate-0">
          {/* Compliant slice - Green */}
          <path
            d={compliantSlice}
            fill="#22c55e"
            stroke="#1f2937"
            strokeWidth="2"
          />
          {/* Non-compliant slice - Red */}
          <path
            d={nonCompliantSlice}
            fill="#ef4444"
            stroke="#1f2937"
            strokeWidth="2"
          />
          {/* Not implemented slice - Gray */}
          <path
            d={notImplementedSlice}
            fill="#6b7280"
            stroke="#1f2937"
            strokeWidth="2"
          />
          {/* Center hole for donut effect */}
          <circle cx="100" cy="100" r="50" fill="#111827" />
        </svg>
        
        {/* Center percentage display */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <span className="text-3xl font-bold text-white">
              {compliancePercentage.toFixed(0)}%
            </span>
            <p className="text-xs text-gray-400">Compliant</p>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
          <span className="text-sm text-gray-300">
            Compliant ({compliant})
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <span className="text-sm text-gray-300">
            Non-Compliant ({nonCompliant})
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-gray-500"></div>
          <span className="text-sm text-gray-300">
            Not Implemented ({notImplemented})
          </span>
        </div>
      </div>
    </div>
  );
};

export default ComplianceChart;