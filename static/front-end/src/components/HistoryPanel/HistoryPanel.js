import React, { useState } from 'react';
import './HistoryPanel.css';
import { FaChevronLeft } from "react-icons/fa";
import { FaAngleRight } from "react-icons/fa6";
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import { HiArrowNarrowRight } from "react-icons/hi";

function HistoryPanel({ history, onSearch }) {
  const [isMinimized, setIsMinimized] = useState(false); // State to track minimized status

  // Toggle the minimized state
  const toggleMinimize = () => setIsMinimized((prev) => !prev);

  return (
    <>
      {/* Maximize Button */}
      {isMinimized && (
        <button className="maximize-btn" onClick={toggleMinimize}>
          <FaAngleRight />
        </button>
      )}

 {/* History Panel */}
 <div className={`history-panel ${isMinimized ? 'hidden' : ''}`}>
        <div className="history-header">
          <h2 className="history-title">Search History</h2>
          <button className="toggle-btn" onClick={toggleMinimize}>
            <FaChevronLeft/>
          </button>
        </div>
        <TransitionGroup className="history-list">
          {history.length === 0 ? (
            <CSSTransition timeout={300} classNames="fade">
              <li className="history-item empty">No recent searches</li>
            </CSSTransition>
          ) : (
            history
              .slice(0)
              .reverse()
              .map((item, index) => (
                <CSSTransition key={index} timeout={500} classNames="fade">
                  <li className="history-item" onClick={() => onSearch(item.query)}>
                   {item.query} 
                  </li>
                </CSSTransition>
              ))
          )}
        </TransitionGroup>
      </div>
    </>
  );
}

export default HistoryPanel;