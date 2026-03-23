import React from 'react';

const BentoCard = ({ title, children, className = '', delay = '0s' }) => {
  return (
    <div 
      className={`bento-card animate-in ${className}`} 
      style={{ animationDelay: delay }}
    >
      {title && <div className="insight-header">{title}</div>}
      <div className="bento-content">
        {children}
      </div>
    </div>
  );
};

export default BentoCard;
