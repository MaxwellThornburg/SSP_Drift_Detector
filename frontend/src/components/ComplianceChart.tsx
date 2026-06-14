import React from 'react';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';

interface ComplianceData {
  compliant: number;
  nonCompliant: number;
  notImplemented: number;
  compliancePercentage: number;
}

interface ComplianceChartProps {
  data: ComplianceData;
}

const COLORS = {
  compliant: '#22c55e',     // Green
  nonCompliant: '#ef4444',  // Red
  indeterminate: '#6b7280', // Gray
  empty: '#cbd5e1'          // Slate for empty state
};

const ComplianceChart: React.FC<ComplianceChartProps> = ({ data }) => {
  const compliant = data.compliant || 0;
  const nonCompliant = data.nonCompliant || 0;
  const notImplemented = data.notImplemented || 0;
  const compliancePercentage = data.compliancePercentage || 0;

  const total = compliant + nonCompliant + notImplemented;

  const chartData = [
    { name: 'Compliant', value: compliant, color: COLORS.compliant },
    { name: 'Non-Compliant', value: nonCompliant, color: COLORS.nonCompliant },
    { name: 'Indeterminate', value: notImplemented, color: COLORS.indeterminate },
  ];

  // Fallback if total is 0
  const displayData = total > 0 ? chartData : [{ name: 'No Data', value: 1, color: COLORS.empty }];

  return (
    <div className="flex flex-col items-center">
      {/* Fixed pixel dimensions prevent the chart from collapsing to 0 */}
      <div className="relative" style={{ width: 256, height: 256 }}>
        
        <PieChart width={256} height={256}>
          <Pie
            data={displayData}
            cx={128} // Center X (half of 256)
            cy={128} // Center Y (half of 256)
            innerRadius={65}
            outerRadius={100}
            paddingAngle={2}
            dataKey="value"
            stroke="none"
            isAnimationActive={true}
          >
            {displayData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          
          {total > 0 && (
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: '1px solid #334155', 
                borderRadius: '8px',
                color: '#f8fafc',
                fontSize: '12px',
                fontWeight: '600'
              }}
              cursor={{ fill: 'rgba(0,0,0,0.05)' }}
            />
          )}
        </PieChart>
        
        {/* Center hole text overlay */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center">
            <span className="text-3xl font-bold text-slate-800">
              {total > 0 ? `${compliancePercentage.toFixed(0)}%` : '0%'}
            </span>
            <p className="text-xs text-slate-500 font-medium">Compliant</p>
          </div>
        </div>
      </div>

      {/* Custom Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS.compliant }}></div>
          <span className="text-sm text-slate-700 font-medium">
            Compliant ({compliant})
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS.nonCompliant }}></div>
          <span className="text-sm text-slate-700 font-medium">
            Non-Compliant ({nonCompliant})
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS.indeterminate }}></div>
          <span className="text-sm text-slate-700 font-medium">
            Indeterminate ({notImplemented})
          </span>
        </div>
      </div>
    </div>
  );
};

export default ComplianceChart;