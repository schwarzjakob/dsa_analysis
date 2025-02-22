import React from "react";

interface DashboardElementProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
}

const DashboardElement: React.FC<DashboardElementProps> = ({
  title,
  children,
  className,
}) => {
  return (
    <div>
      {title ? (
        <div className={`${className} dashboard-card-title`}>{title}</div>
      ) : (
        ""
      )}
      {children}
    </div>
  );
};

export default DashboardElement;
DashboardElement.defaultProps = {
  title: "",
};
