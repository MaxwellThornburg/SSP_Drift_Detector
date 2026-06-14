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

  const displayData = total > 0 ? chartData : [{ name: 'No Data', value: 1, color: COLORS.empty }];

  return (
    <div className="flex flex-col items-center">
      <div style={{ width: 256, height: 256 }}>
        <PieChart width={256} height={256}>
          <Pie
            data={displayData}
            cx={128}
            cy={128}
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
          
          {/* Native SVG text - Bulletproof and guaranteed to render in the center */}
          <text 
            x="50%" 
            y="45%" 
            textAnchor="middle" 
            dominantBaseline="middle" 
            style={{ fontSize: '28px', fontWeight: 'bold', fill: '#1e293b' }}
          >
            {total > 0 ? `${compliancePercentage.toFixed(0)}%` : '0%'}
          </text>
          <text 
            x="50%" 
            y="58%" 
            textAnchor="middle" 
            dominantBaseline="middle" 
            style={{ fontSize: '12px', fontWeight: '500', fill: '#64748b' }}
          >
            Compliant
          </text>

          {total > 0 && (
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff', // Light/White background
                border: '1px solid #cbd5e1', // Light slate border
                borderRadius: '8px',
                color: '#0f172a', // Dark text for high contrast
                fontSize: '12px',
                fontWeight: '600',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
              cursor={{ fill: 'rgba(0,0,0,0.05)' }}
            />
          )}
        </PieChart>
      </div>

      {/* Custom Legend */}
      <div className="mt-8 flex flex-wrap justify-center gap-6">
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