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

  // Calculate angles for conic-gradient
  const compliantAngle = (compliant / total) * 360;
  const nonCompliantAngle = (nonCompliant / total) * 360;
  
  const gradient = `conic-gradient(
    #22c55e 0deg ${compliantAngle}deg,
    #ef4444 ${compliantAngle}deg ${compliantAngle + nonCompliantAngle}deg,
    #6b7280 ${compliantAngle + nonCompliantAngle}deg 360deg
  )`;

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-48 h-48">
        {/* CSS Conic Gradient Donut Chart */}
        <div 
          className="w-full h-full rounded-full"
          style={{ background: total > 0 ? gradient : '#374151' }}
        >
          {/* Center hole for donut effect */}
          <div className="absolute inset-4 rounded-full bg-gray-900 flex items-center justify-center">
            <div className="text-center">
              <span className="text-3xl font-bold text-white">
                {compliancePercentage.toFixed(0)}%
              </span>
              <p className="text-xs text-gray-400">Compliant</p>
            </div>
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