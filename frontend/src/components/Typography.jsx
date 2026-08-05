import React from 'react';
import { cn, useDirectionalReveal } from '../lib/utils';
import { motion } from 'framer-motion';

const revealVariants = {
  hiddenAbove: { opacity: 0, y: -40 },
  hiddenBelow: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.25, 0, 0, 1] } }
};

export const HeroText = ({ children, className, ...props }) => {
  const { ref, animate } = useDirectionalReveal("-100px");
  return (
    <motion.h1
      ref={ref}
      initial="hiddenBelow"
      animate={animate}
      variants={revealVariants}
      className={cn("text-5xl sm:text-6xl md:text-7xl lg:text-[7rem] font-sans tracking-tighter leading-[0.92] font-bold text-foreground", className)}
      {...props}
    >
      {children}
    </motion.h1>
  );
};

export const H1 = ({ children, className, ...props }) => {
  const { ref, animate } = useDirectionalReveal("-50px");
  return (
    <motion.h1
      ref={ref}
      initial="hiddenBelow"
      animate={animate}
      variants={revealVariants}
      className={cn("text-4xl md:text-5xl lg:text-7xl font-sans tracking-tighter leading-tight font-bold text-foreground", className)}
      {...props}
    >
      {children}
    </motion.h1>
  );
};

export const H2 = ({ children, className, ...props }) => {
  const { ref, animate } = useDirectionalReveal("-40px");
  return (
    <motion.h2
      ref={ref}
      initial="hiddenBelow"
      animate={animate}
      variants={{
        ...revealVariants,
        hiddenAbove: { opacity: 0, y: -20 },
        hiddenBelow: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0, 0, 1] } }
      }}
      className={cn("text-2xl md:text-3xl font-sans tracking-tight leading-snug font-bold text-foreground", className)}
      {...props}
    >
      {children}
    </motion.h2>
  );
}; 

export const Body = ({ children, className, ...props }) => (
  <p className={cn("text-base md:text-lg font-sans tracking-normal leading-relaxed text-zinc-400", className)} {...props}>
    {children}
  </p>
);

export const Label = ({ children, className, ...props }) => (
  <span className={cn("font-mono text-xs md:text-sm uppercase tracking-[0.2em] text-[#5568fe] font-bold", className)} {...props}>
    {children}
  </span>
);
  
 